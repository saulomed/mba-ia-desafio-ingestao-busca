# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto demonstra a ingestão de um arquivo PDF para a realização de buscas utilizando Inteligência Artificial.

## Passos de Execução

### 1. Executar o Docker Compose

O primeiro passo é iniciar o container do banco de dados PostgreSQL com a extensão `pgvector` utilizando o Docker Compose.

```bash
docker-compose up -d
```

### 2. Configurar o Ambiente Virtual

Para executar os scripts Python, é necessário criar e ativar um ambiente virtual. Você pode fazer isso de duas maneiras:

**Opção A: Instalando as dependências a partir do `requirements.txt`**

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt
```

**Opção B: Instalando as bibliotecas manualmente**

Caso o arquivo `requirements.txt` não esteja atualizado, você pode instalar as bibliotecas necessárias com o seguinte comando:

```bash
pip install langchain langchain-openai langchain-google-genai langchain-community langchain-text-splitters langchain-postgres "psycopg[binary]" python-dotenv beautifulsoup4 pypdf sentence-transformers transformers pgvector && pip freeze > requirements.txt
```

### 3. Ingerir o Documento

Com o ambiente configurado, execute o script `ingest.py` para processar o `document.pdf` e armazenar os vetores no banco de dados.

```bash
python src/ingest.py
```

### 4. Iniciar o Chat

Após a ingestão, você pode fazer perguntas sobre o conteúdo do documento PDF executando o script `chat.py`.

```bash
python src/chat.py
```

O terminal ficará interativo, e você poderá fazer suas perguntas.

**Exemplo de uso:**

```
--- Chat com Documentos ---
Faça sua pergunta. Digite 'sair' ou 'exit' para terminar.
---------------------------
Faça a sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?

--- Resposta ---

A resposta da IA para a sua pergunta sobre o documento aparecerá aqui.

----------------
Para fazer uma nova pergunta, digite-a abaixo. Para sair, digite 'sair' ou 'exit'.
```
