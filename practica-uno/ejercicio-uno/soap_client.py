from zeep import Client

def suma(a, b):
    client = Client('http://localhost:8000')
    result = client.service.Suma(a, b)
    return result

def resta(a, b):
    client = Client('http://localhost:8000')
    result = client.service.Resta(a, b)
    return result

def multiplicacion(a, b):
    client = Client('http://localhost:8000')
    result = client.service.Multiplicacion(a, b)
    return result

def division(a, b):
    client = Client('http://localhost:8000')
    result = client.service.Division(a, b)
    return result

if __name__ == "__main__":
    print("Suma:", suma(5, 3))
    print("Resta:", resta(5, 3))
    print("Multiplicación:", multiplicacion(5, 3))
    print("División:", division(5, 3))
