import requests

base_url = "http://localhost:8000/pacientes"

# Listar todos los pacientes
response = requests.get(base_url)
if response.status_code == 200:
    print("Listar todos los pacientes:")
    print(response.text)
else:
    print("No hay pacientes registrados.")

# Crear un nuevo paciente
nuevo_paciente = {
    "ci": "1234567",
    "nombre": "Juan",
    "apellido": "Perez",
    "edad": 35,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Perez"
}
response = requests.post(base_url, json=nuevo_paciente)
if response.status_code == 201:
    print("\nCrear un nuevo paciente:")
    print("Paciente creado exitosamente.")
else:
    print("Error al crear el paciente.")

# Buscar paciente por CI
ci_paciente = "123456789"
response = requests.get(f"{base_url}/{ci_paciente}")
if response.status_code == 200:
    print("\nBuscar paciente por CI:")
    print(response.text)
else:
    print("Paciente no encontrado.")

# Listar pacientes con diagnóstico de Diabetes
response = requests.get(f"{base_url}?diagnostico=Diabetes")
if response.status_code == 200:
    print("\nListar pacientes con diagnóstico de Diabetes:")
    print(response.text)
elif response.status_code == 204:
    print("No hay pacientes con diagnóstico de Diabetes.")

# Listar pacientes atendidos por el Doctor Pedro Pérez
response = requests.get(f"{base_url}?doctor=Pedro Perez")
if response.status_code == 200:
    print("\nListar pacientes atendidos por el Doctor Pedro Perez:")
    print(response.text)
elif response.status_code == 204:
    print("No hay pacientes atendidos por el Doctor Pedro Perez.")

# Actualizar información de un paciente
ci_paciente = "1234567"
datos_actualizados = {
    "nombre": "Juan Pablo",
    "edad": 36
}
response = requests.put(f"{base_url}/{ci_paciente}", json=datos_actualizados)
if response.status_code == 200:
    print("\nActualizar información de un paciente:")
    print("Información actualizada exitosamente.")
else:
    print("Error al actualizar la información del paciente.")

# Eliminar un paciente
response = requests.delete(f"{base_url}/{ci_paciente}")
if response.status_code == 200:
    print("\nEliminar un paciente:")
    print("Paciente eliminado exitosamente.")
else:
    print("Error al eliminar el paciente.")
