import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

def ingest_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {pdf_path}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splited_documents = text_splitter.split_documents(documents)
    
    print(f"Splitted documents into {len(splited_documents)} chunks")

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splited_documents
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #embeddings = GoogleGenerativeAIEmbeddings(
    #    model="models/embedding-001",
    #    task_type="RETRIEVAL_DOCUMENT",
    #)
    
    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    #store.add_documents(documents=enriched, ids=ids)
    for i in range(0, len(enriched), 10):  # Lotes de 100 documentos
        store.add_documents(documents=enriched[i:i + 10], ids=ids[i:i + 10])
    
    print(f"Persisted {len(splited_documents)} chunks into the database")


if __name__ == "__main__":
    ingest_pdf(PDF_PATH)
