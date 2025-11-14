import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search import search

def chat():
    """
    Starts an interactive chat session with the user.
    """
    print("--- Chat com Documentos ---")
    print("Faça sua pergunta. Digite 'sair' ou 'exit' para terminar.")
    print("-" * 27)

    while True:
        try:
            query = input("Faça a sua pergunta: ")

            if query.lower() in ["sair", "exit"]:
                print("Encerrando o chat. Até logo!")
                break

            if not query.strip():
                continue

            answer = search(query)
            
            print("\n--- Resposta ---\n")
            print(answer)
            print("\n" + "-" * 16)
            print("Para fazer uma nova pergunta, digite-a abaixo. Para sair, digite 'sair' ou 'exit'.")

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando o chat. Até logo!")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")
            print("Por favor, tente novamente ou digite 'sair' para terminar.")

if __name__ == "__main__":
    chat()
