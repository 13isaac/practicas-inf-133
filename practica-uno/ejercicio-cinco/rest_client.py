import requests

url="http://localhost:8000/"

#lista de animales
response=requests.get(url+"animales")
print("-----lista de animales-----")
print(response.text)

#creando un nuevo animal
create_animal={
    "nombre":"Dondy",
    "especie":"Cocodrilo",
    "genero":"Macho",
    "edad":1,
    "peso":150
}
response_crea=requests.post(url+"animales", json=create_animal)
print("-----creando un nuevo animal-----")
print(response_crea.text)

#buscar danimal por especie
response_especie=requests.get(url+"animales?especie=Tigre")
print("-----filtrando animales por especie-----")
print(response_especie.text)

#filtrar por genero
response_genero=requests.get(url+"animales/?genero=Macho")
print("-----filtrando animales por genero-----")
print(response_genero.text)

#actualizar animal por id
animal_act={
    "nombre":"Spider",
    "especie":"Tarantula",
    "genero":"Hembra",
    "edad":2,
    "peso":1
}
response_act=requests.put(url+"animales/2", json=animal_act)
print("-----actualizar animal por id-----")
print(response_act.text)

#eliminar un animal por id
response_del=requests.delete(url+"animales/2")
print("-----eliminar animal por id-----")
print(response_del.text)
