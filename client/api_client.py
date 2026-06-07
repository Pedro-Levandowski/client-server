"""Cliente HTTP do exemplo Client-Server.

Este módulo representa a parte do Client responsável por se comunicar com o
Server. Ele conhece apenas a interface HTTP exposta pelo servidor e não acessa
diretamente o repositório nem as regras internas da aplicação.
"""

import json
from typing import Dict, List, Tuple
from urllib import error, request


class ApiClient:
    """Encapsula as chamadas HTTP feitas pelo cliente ao servidor."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000") -> None:
        self.base_url = base_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        data: Dict[str, object] | None = None,
    ) -> Tuple[int, Dict[str, object] | List[Dict[str, object]]]:
        """Executa uma requisição HTTP e retorna status code e corpo JSON."""

        url = f"{self.base_url}{path}"
        headers = {"Accept": "application/json"}
        body = None

        if data is not None:
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"

        http_request = request.Request(url=url, data=body, headers=headers, method=method)

        try:
            with request.urlopen(http_request, timeout=5) as response:
                response_body = response.read().decode("utf-8")
                return response.status, json.loads(response_body)
        except error.HTTPError as exc:
            response_body = exc.read().decode("utf-8")
            return exc.code, json.loads(response_body)
        except error.URLError:
            return 503, {
                "error": "Não foi possível conectar ao servidor. Verifique se o Server está em execução."
            }

    def health(self) -> Tuple[int, Dict[str, object]]:
        """Consulta o status do servidor."""

        status, payload = self._request("GET", "/health")
        return status, payload 

    def list_books(self) -> Tuple[int, List[Dict[str, object]]]:
        """Solicita a lista de livros ao servidor."""

        status, payload = self._request("GET", "/books")
        return status, payload

    def get_book(self, book_id: int) -> Tuple[int, Dict[str, object]]:
        """Solicita um livro específico ao servidor."""

        status, payload = self._request("GET", f"/books/{book_id}")
        return status, payload  

    def create_book(self, title: str, author: str, year: int) -> Tuple[int, Dict[str, object]]:
        """Envia dados para cadastrar um novo livro no servidor."""

        status, payload = self._request(
            "POST",
            "/books",
            {"title": title, "author": author, "year": year},
        )
        return status, payload  

    def delete_book(self, book_id: int) -> Tuple[int, Dict[str, object]]:
        """Solicita a remoção de um livro ao servidor."""

        status, payload = self._request("DELETE", f"/books/{book_id}")
        return status, payload
