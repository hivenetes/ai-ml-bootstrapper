from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from retreive_documents import retriever

MODEL = "mistral"
model = Ollama(model=MODEL)

template = """You are an assistant for question-answering tasks. Use the following context to answer the question concisely in three sentences or less. If you don't know, say so.

Context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    | prompt
    | model
    | StrOutputParser()
)

def get_response(query: str) -> str:
    return chain.invoke(query)

if __name__ == "__main__":
    print(get_response("What are GPU Droplets?"))