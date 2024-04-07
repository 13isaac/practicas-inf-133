import requests

url="http://localhost:8000/"

#lista de mensajes
response=requests.get(url+"mensajes")
print("-----lista de mensajes-----")
print(response.text)

#crear un nuevo mensaje
mensaje_n={
    "contenido":"My Country"
}
response_n=requests.post(url+"mensajes", json=mensaje_n)
mensaje_n={
    "contenido":"informatica"
}
response_n=requests.post(url+"mensajes", json=mensaje_n)
mensaje_n={
    "contenido":"sordo mudo"
}
response_n=requests.post(url+"mensajes", json=mensaje_n)
print("-----crear nuevo mensaje-----")
print(response_n.text)

#buscar mensaje por id
response_id=requests.get(url+"mensajes/1")
print("-----buscar mensaje por id-----")
print(response_id.text)

#actualizar mensaje
mensaje_act={
    "contenido":"siempre juntos"
}
response_act=requests.put(url+"mensajes/1",json=mensaje_act)
print("-----actualizar mensaje por id-----")
print(response_act.text)

#iliminar mensaje por id
response_del=requests.delete(url+"mensajes/2")
print("-----eliminar mensaje por id-----")
print(response_del.text)
