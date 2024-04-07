from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse

animales=[
    {
        1:{
            "nombre":"Pedro",
            "especie":"Tigre",
            "genero":"Macho",
            "edad":4,
            "peso":1000
        },
        2:{
            "nombre":"Lucrecia",
            "especie":"Tigre",
            "genero":"Hembra",
            "edad":2,
            "peso":300
        }
    }
]

class AnimalService:
    @staticmethod
    def crear_animal(data):
        id=max(animales[0].keys())+1
        animales[0][id]=data
        return animales
    
    @staticmethod
    def buscar_especie(especie):
        n=[{}]
        lista=animales[0].values()
        for i, animal in enumerate(lista):
            if animal['especie']==especie:
                n[0][i+1]=animales[0][i+1]
        return n
    
    @staticmethod
    def buscar_genero(genero):
        n=[{}]
        lista=animales[0].values()
        for i, animal in enumerate(lista):
            if animal['genero']==genero:
                n[0][i+1]=animales[0][i+1]
        return n

    @staticmethod
    def actualizar_animal(id,data):
        lista=animales[0].keys()
        for i, index in enumerate(lista):
            if index==id:
                animales[0][index].update(data)
                return animales
        return None

    @staticmethod
    def eliminar_animal(id):
        lista=animales[0].keys()
        for i in lista:
            if i==id:
                del animales[0][i]
                return animales
        return None
    
class HTTPResponseHandler:
    @staticmethod
    def respones_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class AnimalRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args,**kwargs):
            self.controller=AnimalService()
            super().__init__(*args,**kwargs)
    #animales?especie={especie}
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path=="/animales":
            if 'especie' in query_params:
                especie=query_params['especie'][0]
                filtrado_especie=self.controller.buscar_especie(especie)
                if filtrado_especie[0]:
                    HTTPResponseHandler.respones_handler(self,200,filtrado_especie)
                else:
                    HTTPResponseHandler.respones_handler(self,404,{"Error":"Especie no encontrada"})
            else:
                HTTPResponseHandler.respones_handler(self,200,animales[0])
        #animales/?genero=Macho
        elif parsed_path.path == "/animales/":
            if 'genero' in query_params:
                genero=query_params['genero'][0]
                filtrado_genero=self.controller.buscar_genero(genero)
                if filtrado_genero[0]:
                    HTTPResponseHandler.respones_handler(self,200,filtrado_genero)
                else:
                    HTTPResponseHandler.respones_handler(self,404,{"Error":"Ningun genero existente"})
        else:
            HTTPResponseHandler.respones_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/animales":
            data=HTTPResponseHandler.read_data(self)
            animal_n=self.controller.crear_animal(data)
            HTTPResponseHandler.respones_handler(self,201,animal_n)
        else:
            HTTPResponseHandler.respones_handler(self,404,{"Error":"Ruta no encontrada"})
    
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            animal_act=self.controller.actualizar_animal(id,data)
            if animal_act:
                HTTPResponseHandler.respones_handler(self,200,animal_act)
            else:
                HTTPResponseHandler.respones_handler(self,404,{"Error":"ID no existente"})
        else:
            HTTPResponseHandler.respones_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id=int(self.path.split("/")[-1])
            animal_del=self.controller.eliminar_animal(id)
            if animal_del:
                HTTPResponseHandler.respones_handler(self,200,animal_del)
            else:
                HTTPResponseHandler.respones_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.respones_handler(self,404,{"Error":"Ruta no encontrada"})
            

def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,AnimalRequestHandler)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
