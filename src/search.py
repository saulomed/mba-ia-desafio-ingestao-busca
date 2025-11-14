import os
import argparse
from dotenv import load_dotenv

from langchain_postgres import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def search(query: str):
    """
    Searches for similar documents in the vector store and uses a language model
    to generate an answer based on the retrieved context.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    retriever = store.as_retriever(search_kwargs={"k": 10})
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.4)

    template = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Elabore a resposta em uma frase completa e de forma cordial.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

EXEMPLO DE RESPOSTA ELABORADA:
Pergunta: "Qual o faturamento da Empresa X?"
Resposta: "O faturamento da Empresa X foi de R$ 500.000.000,00."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
    
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("Buscando documentos e gerando resposta...")
    answer = rag_chain.invoke(query)
    return answer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for documents and answer questions using a LLM.")
    parser.add_argument("query", type=str, help="The query to search for and answer.")
    args = parser.parse_args()

    response = search(args.query)
    print("\n--- Resposta Gerada ---\n")
    print(response)
    print("\n-----------------------\n")
