import requests

url="http://localhost:8000/"

#Mostrar todos los estudiantes
response=requests.get(url+"pacientes/")
print("-----lista de pacientes-----")
print(response.text)

#Crear un paciente
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
print("-----creando un nuevo paciente-----")
print(response_crear.text)

#buscar un paciente por id
response_buscar=requests.get(url+"pacientes/1234567")
print("-----buscar paciente por ci-----")
print(response_buscar.text)

#buscar por diagnostico

response_diagnostico=requests.get(url+"pacientes/?diagnostico=Diabetes")
print("-----buscar pacientes por diagnostico-----")
print(response_diagnostico.text)

#filtrar pacientes por doctor
response_doctor=requests.get(url+"pacientes/?doctor=Pedro Perez")
print("-----buscar pacientes por doctor-----")
print(response_doctor.text)

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

#eliminar paciente por ci
response_elim=requests.delete(url+"pacientes/59203913")
print("-----eliminar paciente-----")
print(response_elim.text)
