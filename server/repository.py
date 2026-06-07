"""Camada de repositório do servidor.

No padrão Client-Server, o servidor centraliza o acesso aos dados. Para manter
o exemplo simples e fácil de apresentar, os dados são guardados em memória.
"""

from typing import Dict, List, Optional

from shared.models import Book


class BookRepository:
    """Armazena e consulta livros em memória."""

    def __init__(self) -> None:
        self._books: Dict[int, Book] = {}
        self._next_id = 1
        self._seed_data()

    def _seed_data(self) -> None:
        """Cria alguns registros iniciais para facilitar a demonstração."""

        self.create("Engenharia de Software", "Ian Sommerville", 2019)
        self.create("Clean Architecture", "Robert C. Martin", 2017)
        self.create("Design Patterns", "Erich Gamma et al.", 1994)

    def list_all(self) -> List[Book]:
        """Retorna todos os livros cadastrados."""

        return list(self._books.values())

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Busca um livro pelo identificador."""

        return self._books.get(book_id)

    def create(self, title: str, author: str, year: int) -> Book:
        """Cadastra um novo livro e retorna o registro criado."""

        book = Book(id=self._next_id, title=title, author=author, year=year)
        self._books[self._next_id] = book
        self._next_id += 1
        return book

    def delete(self, book_id: int) -> bool:
        """Remove um livro quando ele existe."""

        if book_id not in self._books:
            return False

        del self._books[book_id]
        return True
