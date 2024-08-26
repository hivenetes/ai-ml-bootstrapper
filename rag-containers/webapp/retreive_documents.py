import os
import chromadb
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

MODEL = "mistral"
model = Ollama(model=MODEL)

storage_path = os.getenv('CHROMADB_STORAGE_PATH')
if storage_path is None:
    storage_path = "/app/chromadb"

client = chromadb.PersistentClient(path=storage_path)

collection = client.get_collection("gpudroplet_collection")

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    client=client,
    collection_name="gpudroplet_collection",
    embedding_function=embedding_function
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2})

#print(retriever.invoke("What is the cost of H100?"))
#print(retriever.invoke("Is private data shared with third parties or advertisers?"))
#print(retriever.invoke("How does billing work on Paperspace and how can I manage my costs?"))