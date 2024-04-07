import requests
import json

base_url = "http://localhost:8000/pacientes"

class PacienteBuilder:
    def __init__(self):
        self.paciente = {}

    def set_ci(self, ci):
        self.paciente["ci"] = ci
        return self

    def set_nombre(self, nombre):
        self.paciente["nombre"] = nombre
        return self

    def set_apellido(self, apellido):
        self.paciente["apellido"] = apellido
        return self

    def set_edad(self, edad):
        self.paciente["edad"] = edad
        return self

    def set_genero(self, genero):
        self.paciente["genero"] = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.paciente["diagnostico"] = diagnostico
        return self

    def set_doctor(self, doctor):
        self.paciente["doctor"] = doctor
        return self

    def build(self):
        return self.paciente

def print_response(response):
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 201:
        print("Operación exitosa.")
    else:
        print("Error en la operación.")

# Listar todos los pacientes
response = requests.get(base_url)
if response.status_code == 200:
    print("Listar todos los pacientes:")
    print(response.text)
else:
    print("No hay pacientes registrados.")

# Crear un nuevo paciente
nuevo_paciente = PacienteBuilder().set_ci("1234567").set_nombre("Juan").set_apellido("Perez").set_edad(35).set_genero("Masculino").set_diagnostico("Diabetes").set_doctor("Pedro Perez").build()
response = requests.post(base_url, json=nuevo_paciente)
print_response(response)

# Buscar paciente por CI
ci_paciente = "123456789"
response = requests.get(f"{base_url}/{ci_paciente}")
print_response(response)

# Listar pacientes con diagnóstico de Diabetes
response = requests.get(f"{base_url}?diagnostico=Diabetes")
if response.status_code == 200:
    print("Listar pacientes con diagnóstico de Diabetes:")
    print(response.text)
elif response.status_code == 204:
    print("No hay pacientes con diagnóstico de Diabetes.")

# Listar pacientes atendidos por el Doctor Pedro Pérez
response = requests.get(f"{base_url}?doctor=Pedro Perez")
if response.status_code == 200:
    print("Listar pacientes atendidos por el Doctor Pedro Perez:")
    print(response.text)
elif response.status_code == 204:
    print("No hay pacientes atendidos por el Doctor Pedro Perez.")

# Actualizar información de un paciente
ci_paciente = "1234567"
datos_actualizados = {"nombre": "Juan Pablo", "edad": 36}
response = requests.put(f"{base_url}/{ci_paciente}", json=datos_actualizados)
print_response(response)

# Eliminar un paciente
response = requests.delete(f"{base_url}/{ci_paciente}")
print_response(response)
