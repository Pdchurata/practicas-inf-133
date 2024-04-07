from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class PacientesService:
    pacientes = [
        {
            "ci": 123456789,
            "nombre": "Pedrito",
            "apellido": "García",
            "edad": 45,
            "genero": "Masculino",
            "diagnostico": "Fiebre",
            "doctor": "Juan Topo",
        }
    ]

    @staticmethod
    def find_patient(ci):
        return next(
            (paciente for paciente in PacientesService.pacientes if paciente["ci"] == ci),
            None,
        )

    @staticmethod
    def add_patient(data):
        PacientesService.pacientes.append(data)
        return PacientesService.pacientes

    @staticmethod
    def update_patient(ci, data):
        paciente = PacientesService.find_patient(ci)
        if paciente:
            paciente.update(data)
            return PacientesService.pacientes
        else:
            return None

    @staticmethod
    def delete_patient(ci):
        PacientesService.pacientes = [p for p in PacientesService.pacientes if p["ci"] != ci]
        return PacientesService.pacientes

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

        if parsed_path.path == "/pacientes":
            if query_params:
                if "diagnostico" in query_params:
                    diagnostico = query_params["diagnostico"][0]
                    pacientes_filtrados = [paciente for paciente in PacientesService.pacientes if paciente["diagnostico"] == diagnostico]
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                elif "doctor" in query_params:
                    doctor = query_params["doctor"][0]
                    pacientes_filtrados = [paciente for paciente in PacientesService.pacientes if paciente["doctor"] == doctor]
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 200, PacientesService.pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 200, PacientesService.pacientes)
        elif parsed_path.path.startswith("/pacientes/"):
            ci = int(parsed_path.path.split("/")[-1])
            paciente = PacientesService.find_patient(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_patient(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_patient(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = PacientesService.delete_patient(ci)
            HTTPResponseHandler.handle_response(self, 200, pacientes)
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
