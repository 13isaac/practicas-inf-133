from http.server import HTTPServer,BaseHTTPRequestHandler
import json

mensajes=[
    {
        "id":1,
        "contenido":"Hola, mundo!",
        "contenido_encriptado":"Krod, pxqgr!"
    },
]

class MensajeService:
    @staticmethod
    def cifrado_cesar(texto, desplazamiento=3):
        resultado = ""
        for letra in texto:
            if letra.isalpha():
                mayuscula = letra.isupper()
                letra = letra.lower()
                codigo = ord(letra)
                codigo_desplazado = (codigo - 97 + desplazamiento) % 26 + 97
                if mayuscula:
                    resultado += chr(codigo_desplazado).upper()
                else:
                    resultado += chr(codigo_desplazado)
            else:
                resultado += letra
        return resultado

    @staticmethod
    def create_mensaje(mensaje):
        n={}
        cifrado=MensajeService.cifrado_cesar(mensaje)
        id=mensajes[-1]['id']+1
        n['id']=id
        n['contenido']=mensaje
        n['contenido_encriptado']=cifrado
        mensajes.append(n)
        return mensajes
    
    @staticmethod
    def buscar_id(id):
        for i in mensajes:
            if i['id']==id:
                return i
        return None
    
    @staticmethod
    def actualizar_mensaje(id,data):
        for i in mensajes:
            if i['id']==id:
                i.update(data)
                return mensajes
        return None
    
    @staticmethod
    def eliminar_mensaje(id):
        for i,mensaje in enumerate(mensajes):
            if mensaje['id']==id:
                mensajes.pop(i)
                return mensajes
        return None
            
class HTTPResponseHandler():
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
    
class MesanjeHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=MensajeService()
        super().__init__(*args,**kwargs)

    def do_GET(self):
        if self.path == "/mensajes":
            HTTPResponseHandler.response_handler(self,200,mensajes)
        elif self.path.startswith("/mensajes/"):
            id=int(self.path.split("/")[-1])
            mensaje_id=self.controller.buscar_id(id)
            if mensaje_id:
                HTTPResponseHandler.response_handler(self,200,mensaje_id)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path=="/mensajes":
            data=HTTPResponseHandler.read_data(self)
            contenido=data['contenido']
            mensaje_n=self.controller.create_mensaje(contenido)
            HTTPResponseHandler.response_handler(self,201,mensaje_n)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            mensaje_act=self.controller.actualizar_mensaje(id,data)
            if mensaje_act:
                HTTPResponseHandler.response_handler(self,200,mensaje_act)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id=int(self.path.split("/")[-1])
            mensaje_del=self.controller.eliminar_mensaje(id)
            if mensaje_del:
                HTTPResponseHandler.response_handler(self,200,mensaje_del)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})


def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,MesanjeHandler)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
        
