from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse
animales=[
    {
        1:{
            "tipo_animal":"mamifero",
            "nombre":"Pedro",
            "especie":"Tigre",
            "genero":"Macho",
            "edad":4,
            "peso":1000
        },
        2:{
            "tipo_animal":"mamifero",
            "nombre":"Lucrecia",
            "especie":"Mono",
            "genero":"Hembra",
            "edad":2,
            "peso":300
        }
    }
]

class Animal:
    def __init__(self,tipo_animal,nombre,especie,genero,edad,peso):
        self.tipo_animal=tipo_animal
        self.nombre=nombre
        self.especie=especie
        self.genero=genero
        self.edad=edad
        self.peso=peso
#Mamífero, Ave, Reptil, Anfibio o Pez
class Mamifero(Animal):
    def __init__(self,nombre,especie,genero,edad,peso):
        super().__init__("mamifero",nombre,especie,genero,edad,peso)

class Ave(Animal):
    def __init__(self,nombre,especie,genero,edad,peso):
        super().__init__("ave",nombre,especie,genero,edad,peso)

class Reptil(Animal):
    def __init__(self,nombre, especie, genero, edad, peso):
        super().__init__("reptil", nombre, especie, genero, edad, peso)

class Anfibio(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("anfibio", nombre, especie, genero, edad, peso)

class Pez(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("pez", nombre, especie, genero, edad, peso)

#Mamífero, Ave, Reptil, Anfibio o Pez
class AnimalFactory:
    @staticmethod
    def crear_animal(tipo_animal,nombre, especie, genero, edad, peso):
        if tipo_animal == "mamifero":
            return Mamifero(nombre, especie, genero, edad, peso)
        elif tipo_animal == "ave":
            return Ave(nombre, especie, genero, edad, peso)
        elif tipo_animal == "reptil":
            return Reptil(nombre, especie, genero, edad, peso)
        elif tipo_animal == "anifibio":
            return Anfibio(nombre, especie, genero, edad, peso)
        elif tipo_animal == "pez":
            return Pez(nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no valido")
        
class AnimalService:
    def __init__(self):
        self.factory=AnimalFactory()

    def create_animal(self,data):
        tipo_animal=data.get('tipo_animal',None)
        nombre=data.get('nombre',None)
        especie=data.get('especie',None)
        genero=data.get('genero',None)
        edad=data.get('edad',None)
        peso=data.get('edad',None)
        animal=self.factory.crear_animal(
            tipo_animal,nombre,especie,genero,edad,peso
        )
        id=max(animales[0].keys())+1
        animales[0][id]=(animal.__dict__)
        return animal.__dict__
    
    def buscar_especie(self,especie):
        n=[{}]
        lista=animales[0].values()
        for i, animal in enumerate(lista):
            if animal['especie']==especie:
                n[0][i+1]=animal
        return n
    
    def buscar_genero(self,genero):
        n=[{}]
        lista=animales[0].values()
        for i, animal in enumerate(lista):
            if animal['genero']==genero:
                n[0][i+1]=animal
        return n
    
    def actualizar_animal(self,id,data):
        lista=animales[0].keys()
        for i in lista:
            if i==id:
                animales[0][i].update(data)
                return animales
        return None
    
    def borrar_animal(self,id):
        lista=animales[0].keys()
        for i in lista:
            if i==id:
                del animales[0][i]
                return animales
        return None

class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class AnimalHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=AnimalService()
        super().__init__(*args,**kwargs)
    
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        #/animales?especie={especie}
        if parsed_path.path == "/animales":
            if 'especie' in query_params:
                especie=query_params['especie'][0]
                filtrados_esp=self.controller.buscar_especie(especie)
                if filtrados_esp[0]:
                    HTTPResponseHandler.response_handler(self,200,filtrados_esp)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Especie no encontrada"})
            else:
                HTTPResponseHandler.response_handler(self,200,animales)
        #/animales/?genero={genero}
        elif parsed_path.path == "/animales/":
            if 'genero' in query_params:
                genero=query_params['genero'][0]
                filtrados_gen=self.controller.buscar_genero(genero)
                if filtrados_gen[0]:
                    HTTPResponseHandler.response_handler(self,200,filtrados_gen)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Genero no encontrado"})
            else:
                HTTPResponseHandler.response_handler(self,404,animales)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/animales":
            data=HTTPResponseHandler.read_data(self)
            animal_c=self.controller.create_animal(data)
            HTTPResponseHandler.response_handler(self,201,animal_c)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            animal=self.controller.actualizar_animal(id,data)
            if animal:
                HTTPResponseHandler.response_handler(self,200,animal)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrada"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id=int(self.path.split("/")[-1])
            animal=self.controller.borrar_animal(id)
            if animal:
                HTTPResponseHandler.response_handler(self,200,animal)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})


def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,AnimalHandler)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()






