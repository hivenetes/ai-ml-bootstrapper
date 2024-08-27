import os
import uuid
import chromadb
import boto3
import html2text
from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader
from pathlib import Path

storage_path = os.getenv('CHROMADB_STORAGE_PATH', "/app/chromadb")
client = chromadb.PersistentClient(path=storage_path)
collection = client.get_or_create_collection(name="gpudroplet_collection")

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

def upsert_documents(docs, collection):
    for doc in docs:
        print(doc.page_content)
        collection.upsert(
            ids=[str(uuid.uuid4())],
            metadatas=doc.metadata,
            documents=doc.page_content
        )

# Load and process web documents
web_docs = WebBaseLoader(links).load()
web_docs = list(map(clean_html, web_docs))
upsert_documents(web_docs, collection)

def read_secret(secret_name):
    """Reads the secret value from the secret file."""
    secret_path = f"/run/secrets/{secret_name}"
    with open(secret_path, 'r') as secret_file:
        return secret_file.read().strip()

def download_files_from_do_spaces():
    session = boto3.session.Session()
    client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=read_secret('SPACES_KEY'),
                        aws_secret_access_key=read_secret('SPACES_SECRET'))

    Path("pdfs").mkdir(parents=True, exist_ok=True)

    bucket_name = 'ai-ml-bootstrapper-assets'
    for obj in client.list_objects_v2(Bucket=bucket_name)['Contents']:
        file_name = obj['Key']
        client.download_file(bucket_name, file_name, f'pdfs/{file_name}')

def upload_files_to_vector_store():
    # Load and process PDF documents
    pdf_directory = "./pdfs"

    if os.path.exists(pdf_directory):
        pdf_docs = PyPDFDirectoryLoader(pdf_directory).load()
        upsert_documents(pdf_docs, collection)
    else:
        print(f"Warning: The directory '{pdf_directory}' does not exist.")

# Uncomment to test donwload assets
if __name__ == "__main__":
    download_files_from_do_spaces()
    upload_files_to_vector_store()

# Uncomment to query the collection
# results = collection.query(
#     query_texts=["what is the price of VPN Gateway?"], 
#     n_results=1 
# )

# Uncomment to print the collection count
# print(collection.count())