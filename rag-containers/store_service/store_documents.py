import os
import uuid
import chromadb
import boto3
import html2text
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from chromadb.utils import embedding_functions

storage_path = os.getenv('CHROMADB_STORAGE_PATH', "/app/chromadb")
client = chromadb.PersistentClient(path=storage_path)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="gpudroplet_collection", embedding_function=sentence_transformer_ef)

links = ["https://www.digitalocean.com/products/gpu-droplets/"]

def clean_html(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    html.page_content = h.handle(html.page_content)
    
    replacements = {
        "\n": " ",
        "Ä¢": " ",
        "¬†": " ",
        "Â": " ",
        "â€": " ",
        "": " ",
        "?": "? ",
        "Äç": " ",
        "Äî": " "
    }
    for old, new in replacements.items():
        html.page_content = html.page_content.replace(old, new)
    return html

def upsert_documents(docs):
    texts = [doc.page_content for doc in docs]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = []
    for text in texts:
        chunks.extend(text_splitter.split_text(text))

    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    ids = [str(uuid.uuid4()) for _ in chunks]
    embeddings = embedding_model.embed_documents(chunks)
    
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
        
# Load and process web documents
def upload_webpage_content_to_vector_store():
    web_docs = WebBaseLoader(links).load()
    web_docs = list(map(clean_html, web_docs))
    upsert_documents(web_docs)

def read_secrets(file_path):
    """Reads secrets from a file and returns them as a dictionary."""
    secrets = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            secrets[key] = value
    return secrets

def download_files_from_do_spaces():
    secrets_file_path = '/run/secrets/secret'

    secrets = read_secrets(secrets_file_path)

    session = boto3.session.Session()
    client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=secrets.get('DO_SPACES_KEY'),
                        aws_secret_access_key=secrets.get('DO_SPACES_SECRET'))

    Path("pdfs").mkdir(parents=True, exist_ok=True)

    bucket_name = 'ai-ml-bootstrapper-assets'
    for obj in client.list_objects_v2(Bucket=bucket_name)['Contents']:
        file_name = obj['Key']
        client.download_file(bucket_name, file_name, f'pdfs/{file_name}')

def upload_pdf_files_to_vector_store():
    pdf_directory = "./pdfs"

    if os.path.exists(pdf_directory):
        pdf_docs = PyPDFDirectoryLoader(pdf_directory).load()
        upsert_documents(pdf_docs)
    else:
        print(f"Warning: The directory '{pdf_directory}' does not exist.")

# Uncomment to test store documents
if __name__ == "__main__":
    download_files_from_do_spaces()
    upload_webpage_content_to_vector_store()
    upload_pdf_files_to_vector_store()

# Uncomment to query the collection
# results = collection.query(
#     query_texts=["what is the price of VPN Gateway?"], 
#     n_results=1 
# )

# Uncomment to print the collection count
# print(collection.count())