from zeep import Client

client = Client('http://localhost:8000')
result_suma = client.service.Suma(a=5, b=3)
print("Suma:", result_suma)

result_resta = client.service.Resta(a=10, b=4)
print("Resta:", result_resta)

result_multiplicacion = client.service.Multiplicacion(a=7, b=2)
print("Multiplicacion:", result_multiplicacion)

result_division = client.service.Division(a=20, b=5)
print("Division:", result_division)
