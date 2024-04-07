import requests

url="http://localhost:8000/"

#lista de animales
response=requests.get(url+"animales")
print("-----lista de animales-----")
print(response.text)

#crear un nuevo animal
animal_n={
    "tipo_animal":"mamifero",
    "nombre":"Juan",
    "especie":"Serpiente",
    "genero":"Macho",
    "edad":3,
    "peso":5
}
response_n=requests.post(url+"animales", json=animal_n)
print("-----creando un animal-----")
print(response_n.text)

#filtrar animales por especie /animales?especie={especie}
response_esp=requests.get(url+"animales?especie=Tigre")
print("-----filtrando animales por especie-----")
print(response_esp.text)

#filtrando por geenro /animales/?genero={genero}
response_gen=requests.get(url+"/animales/?genero=Macho")
print("-----filtrando animales por genero-----")
print(response_gen.text)

#actualizando un animal
animal_act={
    "tipo_animal":"ave",
    "nombre":"Blue",
    "especie":"Loro",
    "genero":"Macho",
    "edad":1,
    "peso":2
}
response_act=requests.put(url+"animales/1", json=animal_act)
print("-----actualizando animal por id-----")
print(response_act.text)

#eliminar un animal
response_del=requests.delete(url+"animales/3")
print("-----aliminando animal por id-----")
print(response_del.text)
