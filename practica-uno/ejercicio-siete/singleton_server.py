from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

from urllib.parse import urlparse, parse_qs

class GameSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if GameSingleton.__instance is None:
            GameSingleton()
        return GameSingleton.__instance

    def __init__(self):
        if GameSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GameSingleton.__instance = self
            self.choices = ["piedra", "papel", "tijera"]

    def play(self):
        return random.choice(self.choices)


class Partida:
    def __init__(self, id, elemento):
        self.id = id
        self.elemento = elemento
        self.elemento_servidor = GameSingleton.get_instance().play()
        self.resultado = self.calculate_result()

    def calculate_result(self):
        servidor = self.elemento_servidor
        jugador = self.elemento

        if jugador == servidor:
            return "empató"
        elif (jugador == "piedra" and servidor == "tijera") or \
             (jugador == "tijera" and servidor == "papel") or \
             (jugador == "papel" and servidor == "piedra"):
            return "ganó"
        else:
            return "perdió"


class PartidaService:
    partidas = []
    id_counter = 0

    @staticmethod
    def create_partida(data):
        PartidaService.id_counter += 1
        partida = Partida(PartidaService.id_counter, data["elemento"])
        PartidaService.partidas.append(partida)
        return partida

    @staticmethod
    def list_partidas():
        return [partida.__dict__ for partida in PartidaService.partidas]

    @staticmethod
    def list_partidas_resultado(resultado):
        return [partida.__dict__ for partida in PartidaService.partidas if partida.resultado == resultado]


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

        if parsed_path.path == "/partidas":
            if query_params and "resultado" in query_params:
                resultado = query_params["resultado"][0]
                partidas_filtradas = PartidaService.list_partidas_resultado(resultado)
                HTTPResponseHandler.handle_response(self, 200, partidas_filtradas)
            else:
                partidas = PartidaService.list_partidas()
                HTTPResponseHandler.handle_response(self, 200, partidas)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/partidas":
            data = self.read_data()
            partida = PartidaService.create_partida(data)
            HTTPResponseHandler.handle_response(self, 201, partida.__dict__)
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
