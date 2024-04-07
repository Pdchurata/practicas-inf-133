import requests

base_url = "http://localhost:8000/mensajes"

# Listar todos los mensajes
response = requests.get(base_url)
if response.status_code == 200:
    print("Listar todos los mensajes:")
    print(response.json())
else:
    print("No hay mensajes registrados.")

# Crear un nuevo mensaje
nuevo_mensaje = {
    "contenido": "Este es un mensaje secreto"
}
response = requests.post(base_url, json=nuevo_mensaje)
if response.status_code == 201:
    print("\nCrear un nuevo mensaje:")
    print("Mensaje creado exitosamente:")
    print(response.json())
else:
    print("Error al crear el mensaje.")

# Actualizar contenido de un mensaje
id_mensaje = 1  # ID del mensaje de ejemplo
contenido_actualizado = {
    "contenido": "Este es un mensaje modificado"
}
response = requests.put(f"{base_url}/{id_mensaje}", json=contenido_actualizado)
if response.status_code == 200:
    print("\nActualizar contenido de un mensaje:")
    print("Contenido actualizado exitosamente:")
    print(response.json())
else:
    print("Error al actualizar el contenido del mensaje.")

# Buscar mensaje por ID
response = requests.get(f"{base_url}/{id_mensaje}")
if response.status_code == 200:
    print("\nBuscar mensaje por ID:")
    print(response.json())
elif response.status_code == 404:
    print("Mensaje no encontrado.")

# Eliminar un mensaje
response = requests.delete(f"{base_url}/{id_mensaje}")
if response.status_code == 200:
    print("\nEliminar un mensaje:")
    print("Mensaje eliminado exitosamente.")
else:
    print("Error al eliminar el mensaje.")
