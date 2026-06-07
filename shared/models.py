"""Modelos compartilhados entre cliente e servidor.

Neste arquivo ficam estruturas simples usadas para padronizar os dados
transmitidos em JSON. A existência deste módulo ajuda a demonstrar a
organização do projeto e evita duplicação conceitual entre as camadas.
"""

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Book:
    """Representa um livro do catálogo."""

    id: int
    title: str
    author: str
    year: int

    def to_dict(self) -> Dict[str, object]:
        """Converte o livro para dicionário serializável em JSON."""

        return asdict(self)
