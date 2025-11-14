# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.

# Build

Criar e ativar um ambiente virtual (venv):

python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


Split: from langchain_text_splitters import RecursiveCharacterTextSplitter
Embeddings (OpenAI): from langchain_openai import OpenAIEmbeddings
Embeddings (Gemini): from langchain_google_genai import GoogleGenerativeAIEmbeddings
PDF: from langchain_community.document_loaders import PyPDFLoader
Ingestãofrom langchain_postgres import PGVector
Busca: similarity_search_with_score(query, k=10)



pip install langchain langchain-openai langchain-google-genai langchain-community langchain-text-splitters langchain-postgres "psycopg[binary]" python-dotenv beautifulsoup4 pypdf sentence-transformers transformers && pip freeze > requirements.txt
