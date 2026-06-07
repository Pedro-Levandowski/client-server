"""Servidor HTTP do exemplo Client-Server.

Este arquivo representa o componente Server da arquitetura. Ele expõe uma API
HTTP com endpoints para listar, consultar, cadastrar e remover livros. O cliente
não acessa o repositório diretamente; toda comunicação ocorre por requisições
HTTP com mensagens JSON.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server.repository import BookRepository
from server.service import BookService

HOST = "127.0.0.1"
PORT = 8000

repository = BookRepository()
service = BookService(repository)


class ClientServerRequestHandler(BaseHTTPRequestHandler):
    """Manipulador das requisições HTTP recebidas pelo servidor."""

    def _send_json(self, status_code: int, payload: Dict[str, object] | list) -> None:
        """Envia uma resposta JSON ao cliente."""

        response = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _read_json_body(self) -> Tuple[bool, Dict[str, object]]:
        """Lê e interpreta o corpo JSON enviado pelo cliente."""

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return True, {}

        raw_body = self.rfile.read(content_length).decode("utf-8")
        try:
            return True, json.loads(raw_body)
        except json.JSONDecodeError:
            return False, {"error": "JSON inválido no corpo da requisição."}

    def _extract_book_id(self, path: str) -> int | None:
        """Extrai o ID de rotas no formato /books/{id}."""

        parts = path.strip("/").split("/")
        if len(parts) != 2 or parts[0] != "books":
            return None

        try:
            return int(parts[1])
        except ValueError:
            return None

    def do_GET(self) -> None:
        """Processa requisições GET."""

        path = urlparse(self.path).path

        if path == "/health":
            self._send_json(200, {"status": "online", "architecture": "Client-Server"})
            return

        if path == "/books":
            self._send_json(200, service.list_books())
            return

        book_id = self._extract_book_id(path)
        if book_id is not None:
            status_code, payload = service.get_book(book_id)
            self._send_json(status_code, payload)
            return

        self._send_json(404, {"error": "Rota não encontrada."})

    def do_POST(self) -> None:
        """Processa requisições POST."""

        path = urlparse(self.path).path

        if path != "/books":
            self._send_json(404, {"error": "Rota não encontrada."})
            return

        is_valid, data = self._read_json_body()
        if not is_valid:
            self._send_json(400, data)
            return

        status_code, payload = service.create_book(data)
        self._send_json(status_code, payload)

    def do_DELETE(self) -> None:
        """Processa requisições DELETE."""

        path = urlparse(self.path).path
        book_id = self._extract_book_id(path)

        if book_id is None:
            self._send_json(404, {"error": "Rota não encontrada."})
            return

        status_code, payload = service.delete_book(book_id)
        self._send_json(status_code, payload)

    def log_message(self, format: str, *args: object) -> None:
        """Personaliza o log do servidor para facilitar a apresentação."""

        print(f"[SERVER] {self.address_string()} - {format % args}")


def run_server(host: str = HOST, port: int = PORT) -> None:
    """Inicializa o servidor HTTP."""

    server_address = (host, port)
    httpd = HTTPServer(server_address, ClientServerRequestHandler)
    print("Servidor iniciado no padrão Client-Server")
    print(f"Endereço: http://{host}:{port}")
    print("Rotas disponíveis: GET /health, GET /books, GET /books/{id}, POST /books, DELETE /books/{id}")
    print("Pressione Ctrl+C para encerrar.")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
