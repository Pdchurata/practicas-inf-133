from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler
# definimos las funciones de suma, resta, division y multiplicacion como nos pide:
def suma(a, b):
    return a + b
def resta(a, b):
    return a - b
def multiplicacion(a, b):
    return a * b
def division(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b
dispatcher = SoapDispatcher(
    "operaciones-matematicas-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)
# Registramos las funciones para las operaciones matemáticas
dispatcher.register_function(
    "Suma",
    suma,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Resta",
    resta,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Division",
    division,
    returns={"resultado": float},
    args={"a": int, "b": int},
)

# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
