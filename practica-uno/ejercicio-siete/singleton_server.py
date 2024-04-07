from http.server import HTTPServer,BaseHTTPRequestHandler
import json
import random
from urllib.parse import parse_qs,urlparse

partidas=[
    {
        "id":1,
        "elemento":"piedra",
        "elemento_servidor":"papel",
        "resultado":"perdio"
    },
]

class Jugador:
    _instance=None

    def __new__(cls):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    
    def partida(self,elemento,elemento_serv,resultado):
        nueva={}
        id=partidas[-1]['id']+1
        nueva['id']=id
        nueva['elemento']=elemento
        nueva['elemento_servidor']=elemento_serv
        nueva['resultado']=resultado
        partidas.append(nueva)
        return nueva
        
    def jugar(self,elemento):
        resultado={
            "piedrapiedra":"empate",
            "piedrapapel":"gano",
            "piedratijera":"perdio",
            "papelpiedra":"perdio",
            "papelpapel":"empate",
            "papeltijera":"gano",
            "tijerapiedra":"gano",
            "tijerapapel":"perdio",
            "tijeratijera":"empate"
        }
        element_serv=random.choice(["piedra","papel","tijera"])
        juego=element_serv+elemento
        res=self.partida(elemento,element_serv,resultado[juego])
        return res
    
    def filtrar_resultado(self,resultado):
        n=[]
        for i in partidas:
            if i['resultado']==resultado:
                n.append(i)
        return n

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

class JugadorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        #/partidas?resultado={resultado}
        if parsed_path.path == "/partidas":
            if 'resultado' in query_params:
                resultado=query_params['resultado'][0]
                nuevo=player.filtrar_resultado(resultado)
                if nuevo:
                    HTTPResponseHandler.response_handler(self,200,nuevo)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Resultado no encontrado"})
            else:        
                HTTPResponseHandler.response_handler(self,200,partidas)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/partidas":
            data=HTTPResponseHandler.read_data(self)
            nuevo=player.jugar(data['elemento'])
            HTTPResponseHandler.response_handler(self,201,nuevo)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
        

def main(port=8000):
    global player
    player=Jugador()

    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,JugadorHandler)
        print(f'Iniciando el servidor en el puerto {port}....')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
