import requests

url="http://localhost:8000/graphql"

query="""
    {
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response=requests.post(url,json={'query':query})
print("-----lista de plantas-----")
print(response.text)

#------------crear una planta--------------
#nombre, especie, edad, altura, frutos
query_crear="""
mutation{
    crearPlanta(nombre:"Manzana", especie:"Malus", edad: 1, altura: 45.5, frutos: false){
        planta{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_crear=requests.post(url, json={'query':query_crear})
print("-----crear planta-----")
print(response_crear.text)

#Buscar planta por especie buscar_por_especie
query_especie="""
    {
        buscarPorEspecie(especie:"Malus"){
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response_especie=requests.post(url, json={'query':query_especie})
print("-----buscar planta por especie-----")
print(response_especie.text)

#buscar la plantas que tienen frutos buscar_frutos
query_frutos="""
    {
        buscarFrutos{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response_frutos=requests.post(url, json={'query':query_frutos})
print("-----buscar plantas que tienen frutos-----")
print(response_frutos.text)

#actualizar_planta id, nombre, especie, edad, altura, frutos
query_actualizar="""
mutation{
    actualizarPlanta(id: 2, nombre:"Margarita", especie:"Bellis", edad:6, altura: 20.2, frutos: false){
        planta{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_actualizar=requests.post(url, json={'query':query_actualizar})
print("-----actualizar planta-----")
print(response_actualizar.text)

#eliminar_planta
query_eliminar="""
mutation{
    eliminarPlanta(id:2){
        planta{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_eliminar=requests.post(url, json={'query':query_eliminar})
print("-----eliminar planta-----")
print(response_eliminar.text)

response=requests.post(url,json={'query':query})
print("-----lista de plantas-----")
print(response.text)
