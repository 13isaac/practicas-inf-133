from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int,Boolean,Float, List, Schema, Field, Mutation

###############################################
class Planta(ObjectType):
    id = Int()
    nombre=String() #nombre pupular
    especie=String() #nombre cientifico
    edad=Int()
    altura=Float()
    frutos=Boolean()
######################################################
plantas=[
            Planta(id=1, nombre="Rosa", especie="Rosa spp", edad=3, altura=54.2, frutos=True),
            Planta(id=2, nombre="Limon", especie="Citrus Limon", edad=7, altura=104.3, frutos=True),
        ]
###############################################
class Query(ObjectType):
    plantas=List(Planta)
    buscar_por_especie=Field(Planta, especie=String())
    buscar_frutos=List(Planta)

    def resolve_plantas(root, info):
        return plantas

    def resolve_buscar_por_especie(root, info, especie):
        for i in plantas:
            if i.especie == especie:
                return i
        return None
    
    def resolve_buscar_frutos(root, info):
        n=[]
        for i in plantas:
            if i.frutos:
                n.append(i)
        return n
###################################################    
class CrearPlanta(Mutation):
    class Arguments:
        nombre=String()
        especie=String()
        edad=Int()
        altura=Float()
        frutos=Boolean()
    planta=Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta=Planta(
            id=max([i.id for i in plantas])+1,
            nombre=nombre,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
    
class ActualizarPlanta(Mutation):
    class Arguments:
        id=Int()
        nombre=String()
        especie=String()
        edad=Int()
        altura=Float()
        frutos=Boolean()
    planta=Field(Planta)

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for i in plantas:
            if i.id == id:
                i.nombre=nombre
                i.especie=especie
                i.edad=edad
                i.altura=altura
                i.frutos=frutos
                return ActualizarPlanta(planta=i)
        return None
    
class EliminarPlanta(Mutation):
    class Arguments:
        id=Int()
    planta=Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return EliminarPlanta(planta=planta)
        return None
#################################################
class Mutations(ObjectType):
    crear_planta=CrearPlanta.Field()
    actualizar_planta=ActualizarPlanta.Field()
    eliminar_planta=EliminarPlanta.Field()
################################################
schema=Schema(query=Query, mutation=Mutations)
#################################################
class HTTPResponseHandler():
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))
    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers["Content-Length"])
        post_data=handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
###########################################
class GraphQLRequestPlantas(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/graphql":
            result=HTTPResponseHandler.read_data(self)
            result=schema.execute(result["query"])
            HTTPResponseHandler.response_handler(self,200,result.data)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error","Ruta no encontrada"})
###########################################
def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,GraphQLRequestPlantas)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
