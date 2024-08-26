import os
import uuid
import chromadb
from langchain_community.document_loaders import WebBaseLoader, PyPDFDirectoryLoader
import html2text

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

# Load and process PDF documents
pdf_directory = "/app/chromadb/pdfs/"
if os.path.exists(pdf_directory):
    pdf_docs = PyPDFDirectoryLoader(pdf_directory).load()
    upsert_documents(pdf_docs, collection)
else:
    print(f"Warning: The directory '{pdf_directory}' does not exist.")

# Uncomment to query the collection
# results = collection.query(
#     query_texts=["what is the price of VPN Gateway?"], 
#     n_results=1 
# )

# Uncomment to print the collection count
# print(collection.count())