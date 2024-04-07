from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field
class Planta(ObjectType):
    id = Int()
    nombre_comun = String()
    especie = String()
    edad_meses = Int()
    altura_cm = Int()
    frutos = Boolean()
class Query(ObjectType):
    plantas = List(Planta)
    plantas_por_especie = List(Planta, especie=String())
    plantas_con_frutos = List(Planta)
    def resolve_plantas(root, info):
        return plantas
    def resolve_plantas_por_especie(root, info, especie):
        return [planta for planta in plantas if planta.especie == especie]
    def resolve_plantas_con_frutos(root, info):
        return [planta for planta in plantas if planta.frutos]
plantas = [
    Planta(id=1, nombre_comun="Cactus", especie="Cactaceae", edad_meses=12, altura_cm=20, frutos=False),
    Planta(id=2, nombre_comun="Tomate", especie="Solanum lycopersicum", edad_meses=6, altura_cm=30, frutos=True),
]
schema = Schema(query=Query)
class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()
if __name__ == "__main__":
    run_server()