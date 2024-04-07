import requests

url="http://localhost:8000/"

#listar todas las partidas
response=requests.get(url+"partidas")
print("-----lista de partidas-----")
print(response.text)

#crear partidas
partida_n={
    "elemento":"piedra"
}
response_n=requests.post(url+"partidas",json=partida_n)
print("-----creando partida-----")
print(response_n.text)

partida_n={
    "elemento":"papel"
}
response_n=requests.post(url+"partidas",json=partida_n)
print("-----creando partida-----")
print(response_n.text)

partida_n={
    "elemento":"tijera"
}
response_n=requests.post(url+"partidas",json=partida_n)
print("-----creando partida-----")
print(response_n.text)
#partidas ganadas /partidas?resultado={resultado}
response_g=requests.get(url+"partidas?resultado=gano")
print("-----partidas ganadas-----")
print(response_g.text)

#partidas perdidas
response_p=requests.get(url+"partidas?resultado=perdio")
print("-----partidas perdidas-----")
print(response_p.text)

#listar todas las partidas
response=requests.get(url+"partidas")
print("-----lista de partidas-----")
print(response.text)
