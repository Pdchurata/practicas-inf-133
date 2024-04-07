from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, **kwargs):
        if animal_type == "Mamifero":
            return Mamifero(**kwargs)
        elif animal_type == "Ave":
            return Ave(**kwargs)
        elif animal_type == "Reptil":
            return Reptil(**kwargs)
        elif animal_type == "Anfibio":
            return Anfibio(**kwargs)
        elif animal_type == "Pez":
            return Pez(**kwargs)
        else:
            raise ValueError("Tipo de animal no válido")

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso


class Mamifero(Animal):
    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)
        self.tipo = "Mamífero"


class Ave(Animal):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.tipo = "Ave"

class Reptil(Animal):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.tipo = "Reptil"

class Anfibio(Animal):
    def __init__(self, id,**kwargs):
        super().__init__(**kwargs)
        self.tipo = "Anfibio"

class Pez(Animal):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.tipo = "Pez"

class AnimalesService:
    animales = []
    id_counter = 0

    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in AnimalesService.animales if animal["id"] == id),
            None,
        )

    @staticmethod
    def add_animal(data):
        AnimalesService.id_counter += 1
        data["id"] = AnimalesService.id_counter
        animal_type = data.pop("tipo")
        animal = AnimalFactory.create_animal(animal_type, **data)
        AnimalesService.animales.append(animal.__dict__)
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
            for key, value in data.items():
                animal[key] = value
            return AnimalesService.animales
        else:
            return None

    @staticmethod
    def delete_animal(id):
        AnimalesService.animales = [a for a in AnimalesService.animales if a["id"] != id]
        return AnimalesService.animales
    
def initialize_animals():
    if not AnimalesService.animales:
        ejemplo_animal = {
            "id": 1,
            "nombre": "León",
            "especie": "Panthera leo",
            "genero": "Masculino",
            "edad": 5,
            "peso": 180,
            "tipo": "Mamifero"  # Agregar el campo "tipo" con el valor correspondiente
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            animales = AnimalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animales)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode("utf-8"))
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
    run_server()
