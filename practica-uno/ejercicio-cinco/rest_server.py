from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class AnimalesService:
    animales = []

    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in AnimalesService.animales if animal["id"] == id),
            None,
        )

    @staticmethod
    def add_animal(data):
        data["id"] = len(AnimalesService.animales) + 1
        AnimalesService.animales.append(data)
        return AnimalesService.animales

    @staticmethod
    def filter_animals_by_species(especie):
        return [
            animal for animal in AnimalesService.animales if animal["especie"] == especie
        ]

    @staticmethod
    def filter_animals_by_gender(genero):
        return [
            animal for animal in AnimalesService.animales if animal["genero"] == genero
        ]

    @staticmethod
    def update_animal(id, data):
        animal = AnimalesService.find_animal(id)
        if animal:
            animal.update(data)
            return AnimalesService.animales
        else:
            return None

    @staticmethod
    def delete_animal(id):
        AnimalesService.animales = [a for a in AnimalesService.animales if a["id"] != id]
        return AnimalesService.animales

def initialize_animals():
    if not AnimalesService.animales:
    # Crear un animal de ejemplo
    
     ejemplo_animal = {
        "id": 1,
        "nombre": "León",
        "especie": "Panthera leo",
        "genero": "Masculino",
        "edad": 5,
        "peso": 180
    }
    AnimalesService.add_animal(ejemplo_animal)

initialize_animals()

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
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if query_params:
                if "especie" in query_params:
                    especie = query_params["especie"][0]
                    animales_filtrados = AnimalesService.filter_animals_by_species(especie)
                    HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
                elif "genero" in query_params:
                    genero = query_params["genero"][0]
                    animales_filtrados = AnimalesService.filter_animals_by_gender(genero)
                    HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 200, AnimalesService.animales)
            else:
                HTTPResponseHandler.handle_response(self, 200, AnimalesService.animales)
        elif parsed_path.path.startswith("/animales/"):
            id = int(parsed_path.path.split("/")[-1])
            animal = AnimalesService.find_animal(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, [animal])
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animales = AnimalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animales)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales = AnimalesService.update_animal(id, data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales = AnimalesService.delete_animal(id)
            HTTPResponseHandler.handle_response(self, 200, animales)
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
