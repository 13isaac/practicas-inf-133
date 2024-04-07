import requests

url="http://localhost:8000/"

response=requests.get(url+"pacientes/")
print("-----lista de pacientes-----")
print(response.text)

#crear un paciente
crear_paciente={
        "ci":10384723,
        "nombre":"Maria",
        "apellido":"Perez",
        "edad":12,
        "genero":"Femenino",
        "diagnostico":"Diabetes",
        "doctor":"Pedro Perez"
}
response_crear=requests.post(url+"pacientes", json=crear_paciente)
print("-----crear paciente-----")
print(response_crear.text)

#buscar paciente por ci
response_ci=requests.get(url+"pacientes/10384723")
print("-----buscar paciente por ci-----")
print(response_ci.text)

#filtrar pacientes por diagnostico
response_diag=requests.get(url+"pacientes/?diagnostico=Diabetes")
print("-----filtar pacientes por diagnostico-----")
print(response_diag.text)

#filtrar por doctor
response_doc=requests.get(url+"pacientes/?doctor=Pedro Perez")
print("-----filtar pacientes por doctor-----")
print(response_doc.text)

#actualizar la info de un paciente
act_paciente={
    "ci":59203913,
    "nombre":"Pedro",
    "apellido":"Infante",
    "edad":12,
    "genero":"Masculino",
    "diagnostico":"Gripe",
    "doctor":"Mario Celso"
}
response_act=requests.put(url+"pacientes/1234567", json=act_paciente)
print("-----actualizar paciente-----")
print(response_act.text)

#eliminar un paciente por si
response_del=requests.delete(url+"pacientes/10384723")
print("-----eliminar paciente-----")
print(response_del.text)
