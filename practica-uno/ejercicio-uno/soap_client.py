from zeep import Client

client=Client('http://localhost:8000')
result=client.service.Suma(a=5,b=3)
print("---suma---")
print(result)

result=client.service.Resta(a=5,b=3)
print("---reta---")
print(result)

result=client.service.Multiplicacion(a=5,b=3)
print("---multiplicacion---")
print(result)

result=client.service.Division(a=5,b=3)
print("---division---")
print(result)
