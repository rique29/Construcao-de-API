livros = [
    {"id": 1, "title": "O Senhor dos Anéis", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "Dom Casmurro", "author": "Machado de Assis"}
]

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class APILivros(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(livros).encode('utf-8'))
        elif self.path.startswith('/books/'):
            try:
                id_livro = int(self.path.split('/')[-1])
            except ValueError:
                self.send_response(400) # Bad Request se o ID não for um número
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"erro": "ID inválido"}).encode('utf-8'))
            else:
                livro_encontrado = next((livro for livro in livros if livro["id"] == id_livro), None)
                if livro_encontrado:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(livro_encontrado).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"erro": "Livro não encontrado"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                novo_livro_data = json.loads(post_data.decode('utf-8'))
                title = novo_livro_data.get("title")
                author = novo_livro_data.get("author")

                if title and author:
                    novo_livro = {
                        "id": len(livros) + 1,
                        "title": title,
                        "author": author
                    }
                    livros.append(novo_livro)

                    self.send_response(201)  # Created
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(novo_livro).encode('utf-8'))
                else:
                    self.send_response(400)  # Bad Request
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"erro": "Payload deve conter 'title' e 'author'"}).encode('utf-8'))

            except json.JSONDecodeError:
                self.send_response(400)  # Bad Request
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"erro": "Payload JSON inválido"}).encode('utf-8'))

            except Exception as e:
                self.send_response(500)  # Internal Server Error
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"erro": "Erro interno do servidor", "detalhes": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APILivros)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()


