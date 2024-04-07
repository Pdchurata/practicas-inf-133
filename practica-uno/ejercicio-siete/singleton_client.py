import requests

base_url = "http://localhost:8000/partidas"

# Listar todas las partidas
response = requests.get(base_url)
if response.status_code == 200:
    print("Listar todas las partidas:")
    print(response.json())
else:
    print("No hay partidas registradas.")

# Crear una nueva partida
nueva_partida = {
    "elemento": "piedra"
}
response = requests.post(base_url, json=nueva_partida)
if response.status_code == 201:
    print("\nCrear una nueva partida:")
    print("Partida creada exitosamente:")
    print(response.json())
else:
    print("Error al crear la partida.")

# Listar partidas ganadas
response = requests.get(f"{base_url}?resultado=ganó")
if response.status_code == 200:
    print("\nListar partidas ganadas:")
    print(response.json())
else:
    print("No hay partidas ganadas.")

# Listar partidas perdidas
response = requests.get(f"{base_url}?resultado=perdió")
if response.status_code == 200:
    print("\nListar partidas perdidas:")
    print(response.json())
else:
    print("No hay partidas perdidas.")
