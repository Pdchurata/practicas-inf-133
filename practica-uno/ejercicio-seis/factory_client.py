import requests

base_url = "http://localhost:8000/animales"

# Listar todos los animales
response = requests.get(base_url)
if response.status_code == 200:
    print("Listar todos los animales:")
    print(response.json())
else:
    print("No hay animales registrados.")

# Crear un nuevo animal
nuevo_animal = {
    "nombre": "Elefante",
    "especie": "Loxodonta africana",
    "genero": "Femenino",
    "edad": 10,
    "peso": 4000,
    "tipo": "Mamífero"
}
response = requests.post(base_url, json=nuevo_animal)
if response.status_code == 201:
    print("\nCrear un nuevo animal:")
    print("Animal creado exitosamente:")
    print(response.json())
else:
    print("Error al crear el animal.")

# Buscar animales por especie
especie = "Loxodonta africana"
response = requests.get(f"{base_url}?especie={especie}")
if response.status_code == 200:
    print("\nBuscar animales por especie:")
    print(response.json())
elif response.status_code == 204:
    print("No hay animales de esa especie.")

# Buscar animales por género
genero = "Femenino"
response = requests.get(f"{base_url}?genero={genero}")
if response.status_code == 200:
    print("\nBuscar animales por género:")
    print(response.json())
elif response.status_code == 204:
    print("No hay animales de ese género.")

# Actualizar información de un animal
id_animal = 1  # ID del animal de ejemplo
datos_actualizados = {
    "nombre": "León Africano",
    "edad": 7
}
response = requests.put(f"{base_url}/{id_animal}", json=datos_actualizados)
if response.status_code == 200:
    print("\nActualizar información de un animal:")
    print("Información actualizada exitosamente:")
    print(response.json())
else:
    print("Error al actualizar la información del animal.")

# Eliminar un animal
response = requests.delete(f"{base_url}/{id_animal}")
if response.status_code == 200:
    print("\nEliminar un animal:")
    print("Animal eliminado exitosamente.")
    print("Animales restantes:")
    print(response.json())
else:
    print("Error al eliminar el animal.")
