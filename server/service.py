"""Camada de serviço do servidor.

Esta camada concentra as regras de negócio do sistema. Assim, a camada HTTP
fica responsável apenas por receber requisições e devolver respostas, mantendo
uma separação clara de responsabilidades.
"""

from typing import Dict, List, Tuple

from server.repository import BookRepository


class BookService:
    """Executa as operações de negócio do catálogo de livros."""

    def __init__(self, repository: BookRepository) -> None:
        self.repository = repository

    def list_books(self) -> List[Dict[str, object]]:
        """Lista todos os livros cadastrados."""

        return [book.to_dict() for book in self.repository.list_all()]

    def get_book(self, book_id: int) -> Tuple[int, Dict[str, object]]:
        """Busca um livro específico e retorna código HTTP e corpo da resposta."""

        book = self.repository.find_by_id(book_id)
        if book is None:
            return 404, {"error": "Livro não encontrado."}

        return 200, book.to_dict()

    def create_book(self, data: Dict[str, object]) -> Tuple[int, Dict[str, object]]:
        """Valida os dados recebidos e cadastra um novo livro."""

        required_fields = ["title", "author", "year"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return 400, {
                "error": "Campos obrigatórios ausentes.",
                "missing_fields": missing_fields,
            }

        title = str(data["title"]).strip()
        author = str(data["author"]).strip()

        try:
            year = int(data["year"])
        except (TypeError, ValueError):
            return 400, {"error": "O campo 'year' deve ser um número inteiro."}

        if not title or not author:
            return 400, {"error": "Título e autor não podem ser vazios."}

        if year < 0:
            return 400, {"error": "O ano não pode ser negativo."}

        created_book = self.repository.create(title=title, author=author, year=year)
        return 201, created_book.to_dict()

    def delete_book(self, book_id: int) -> Tuple[int, Dict[str, object]]:
        """Remove um livro específico."""

        removed = self.repository.delete(book_id)
        if not removed:
            return 404, {"error": "Livro não encontrado."}

        return 200, {"message": "Livro removido com sucesso."}
