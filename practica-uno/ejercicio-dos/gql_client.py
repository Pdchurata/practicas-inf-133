import requests
# URL del servidor gql
url = 'http://localhost:8000/graphql'
# Consulta gql para listar todas las plantas
listar_plantas_query = """
    query {
        plantas {
            id
            nombreComun
            especie
            edadMeses
            alturaCm
            frutos
        }
    }
"""
# Consulta gql para buscar plantas por especie
buscar_por_especie_query = """
    query BuscarPorEspecie($especie: String!) {
        plantasPorEspecie(especie: $especie) {
            id
            nombreComun
            especie
            edadMeses
            alturaCm
            frutos
        }
    }
"""
# Consulta gql para buscar plantas que tienen frutos
buscar_con_frutos_query = """
    query {
        plantasConFrutos {
            id
            nombreComun
            especie
            edadMeses
            alturaCm
            frutos
        }
    }
"""
# Mutación gql para crear una nueva planta
crear_planta_mutation = """
    mutation CrearPlanta($input: PlantaInput!) {
        crearPlanta(input: $input) {
            planta {
                id
                nombreComun
                especie
                edadMeses
                alturaCm
                frutos
            }
        }
    }
"""
# Mutación gql para actualizar la información de una planta
actualizar_planta_mutation = """
    mutation ActualizarPlanta($input: PlantaInput!) {
        actualizarPlanta(input: $input) {
            planta {
                id
                nombreComun
                especie
                edadMeses
                alturaCm
                frutos
            }
        }
    }
"""
# Mutación gql para eliminar una planta
eliminar_planta_mutation = """
    mutation EliminarPlanta($id: Int!) {
        eliminarPlanta(id: $id) {
            message
        }
    }
"""
# Función para enviar una solicitud gql
def enviar_solicitud(query, variables=None):
    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.ok:
        return response.json()
    else:
        print("Error al procesar la solicitud:", response.text)
        return None
# Función para imprimir el resultado de la consulta
def imprimir_resultado(resultado, operacion):
    if resultado and operacion in resultado:
        print(operacion.capitalize() + ":", resultado[operacion])
# Listar todas las plantas
resultado_listar_plantas = enviar_solicitud(listar_plantas_query)
imprimir_resultado(resultado_listar_plantas, "plantas")
# Buscar plantas por especie
especie_buscar = "Cactaceae"
resultado_buscar_por_especie = enviar_solicitud(buscar_por_especie_query, {"especie": especie_buscar})
imprimir_resultado(resultado_buscar_por_especie, "plantasPorEspecie")
# Buscar plantas que tienen frutos
resultado_buscar_con_frutos = enviar_solicitud(buscar_con_frutos_query)
imprimir_resultado(resultado_buscar_con_frutos, "plantasConFrutos")
# Crear una nueva planta
nueva_planta = {
    "input": {
        "nombreComun": "Rosa",
        "especie": "Rosa gallica",
        "edadMeses": 8,
        "alturaCm": 25,
        "frutos": False
    }
}
resultado_crear_planta = enviar_solicitud(crear_planta_mutation, nueva_planta)
imprimir_resultado(resultado_crear_planta, "crearPlanta")
# Actualizar la información de una planta
planta_actualizada = {
    "input": {
        "id": 1,
        "nombreComun": "Cactus de Navidad",
        "especie": "Schlumbergera truncata",
        "edadMeses": 14,
        "alturaCm": 22,
        "frutos": False
    }
}
resultado_actualizar_planta = enviar_solicitud(actualizar_planta_mutation, planta_actualizada)
imprimir_resultado(resultado_actualizar_planta, "actualizarPlanta")
# Eliminar una planta
id_planta_eliminar = 2
resultado_eliminar_planta = enviar_solicitud(eliminar_planta_mutation, {"id": id_planta_eliminar})
imprimir_resultado(resultado_eliminar_planta, "eliminarPlanta")
