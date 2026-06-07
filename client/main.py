"""Aplicação Client do exemplo Client-Server.

Este arquivo representa a interface utilizada pelo usuário. Ele envia comandos
ao servidor por HTTP e exibe as respostas recebidas, demonstrando que o cliente
consome serviços oferecidos por um servidor separado.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from client.api_client import ApiClient


def print_json(title: str, status_code: int, payload: Dict[str, object] | List[Dict[str, object]]) -> None:
    """Exibe respostas do servidor em formato legível."""

    print(f"\n=== {title} ===")
    print(f"Status HTTP: {status_code}")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def run_demo(api_client: ApiClient) -> None:
    """Executa um roteiro automático para apresentação em seminário."""

    status, payload = api_client.health()
    print_json("1. Cliente verifica se o servidor está online", status, payload)

    status, payload = api_client.list_books()
    print_json("2. Cliente solicita lista de livros", status, payload)

    status, payload = api_client.create_book(
        title="Padrões Arquiteturais na Prática",
        author="Grupo do Seminário",
        year=2026,
    )
    print_json("3. Cliente cadastra um novo livro", status, payload)

    created_book_id = int(payload["id"]) if status == 201 and isinstance(payload, dict) else 1

    status, payload = api_client.get_book(created_book_id)
    print_json("4. Cliente busca o livro recém-cadastrado", status, payload)

    status, payload = api_client.delete_book(created_book_id)
    print_json("5. Cliente solicita a remoção do livro", status, payload)

    status, payload = api_client.list_books()
    print_json("6. Cliente solicita a lista atualizada", status, payload)


def show_menu() -> None:
    """Mostra as opções disponíveis ao usuário."""

    print("\n=== Cliente do Catálogo de Livros ===")
    print("1. Verificar status do servidor")
    print("2. Listar livros")
    print("3. Buscar livro por ID")
    print("4. Cadastrar livro")
    print("5. Remover livro")
    print("0. Sair")


def run_interactive(api_client: ApiClient) -> None:
    """Executa o cliente em modo interativo."""

    while True:
        show_menu()
        option = input("Escolha uma opção: ").strip()

        if option == "0":
            print("Cliente encerrado.")
            break

        if option == "1":
            status, payload = api_client.health()
            print_json("Status do servidor", status, payload)

        elif option == "2":
            status, payload = api_client.list_books()
            print_json("Lista de livros", status, payload)

        elif option == "3":
            book_id = int(input("Informe o ID do livro: "))
            status, payload = api_client.get_book(book_id)
            print_json("Busca de livro", status, payload)

        elif option == "4":
            title = input("Título: ").strip()
            author = input("Autor: ").strip()
            year = int(input("Ano: "))
            status, payload = api_client.create_book(title, author, year)
            print_json("Cadastro de livro", status, payload)

        elif option == "5":
            book_id = int(input("Informe o ID do livro: "))
            status, payload = api_client.delete_book(book_id)
            print_json("Remoção de livro", status, payload)

        else:
            print("Opção inválida. Tente novamente.")


def parse_args() -> argparse.Namespace:
    """Lê argumentos de linha de comando."""

    parser = argparse.ArgumentParser(description="Cliente do exemplo Client-Server")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="URL base do servidor. Padrão: http://127.0.0.1:8000",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Executa uma demonstração automática sem menu interativo.",
    )
    return parser.parse_args()


def main() -> None:
    """Ponto de entrada do cliente."""

    args = parse_args()
    api_client = ApiClient(base_url=args.base_url)

    if args.demo:
        run_demo(api_client)
    else:
        run_interactive(api_client)


if __name__ == "__main__":
    main()
