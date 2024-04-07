from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class MessageService:
    messages = []

    @staticmethod
    def find_message(id):
        return next(
            (message for message in MessageService.messages if message["id"] == id),
            None,
        )

    @staticmethod
    def add_message(data):
        data["id"] = len(MessageService.messages) + 1
        data["contenido_encriptado"] = MessageService.encrypt_message(data["contenido"])
        MessageService.messages.append(data)
        return MessageService.messages

    @staticmethod
    def update_message(id, data):
        message = MessageService.find_message(id)
        if message:
            message.update(data)
            message["contenido_encriptado"] = MessageService.encrypt_message(data["contenido"])
            return MessageService.messages
        else:
            return None

    @staticmethod
    def delete_message(id):
        MessageService.messages = [m for m in MessageService.messages if m["id"] != id]
        return MessageService.messages

    @staticmethod
    def encrypt_message(message):
        encrypted_message = ""
        for char in message:
            if char.isalpha():
                char_code = ord(char)
                encrypted_char_code = (char_code - ord("a") + 3) % 26 + ord("a")
                encrypted_char = chr(encrypted_char_code)
                encrypted_message += encrypted_char
            else:
                encrypted_message += char
        return encrypted_message

def initialize_messages():
    if not MessageService.messages:
        example_message = {
            "id": 1,
            "contenido": "Este es un mensaje de ejemplo"
        }
        MessageService.add_message(example_message)

initialize_messages()

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 200, MessageService.messages)
        elif parsed_path.path.startswith("/mensajes/"):
            id = int(parsed_path.path.split("/")[-1])
            message = MessageService.find_message(id)
            if message:
                HTTPResponseHandler.handle_response(self, 200, message)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            messages = MessageService.add_message(data)
            HTTPResponseHandler.handle_response(self, 201, messages)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            messages = MessageService.update_message(id, data)
            if messages:
                HTTPResponseHandler.handle_response(self, 200, messages)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            messages = MessageService.delete_message(id)
            HTTPResponseHandler.handle_response(self, 200, messages)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    # Iniciar el servidor
    run_server()
