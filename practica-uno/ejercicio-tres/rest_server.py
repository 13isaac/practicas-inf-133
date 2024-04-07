from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse

pacientes=[
        {
            "ci":1234567,
            "nombre":"Carlos",
            "apellido":"Garcia",
            "edad":33,
            "genero":"Masculino",
            "diagnostico":"Enfermo",
            "doctor":"Pedro Perez"
        },
        {
            "ci":98535731,
            "nombre":"Nancy",
            "apellido":"Mullisaca",
            "edad":22,
            "genero":"Femenino",
            "diagnostico":"Diabetes",
            "doctor":"Mario Celso"
        }
]

class PacienteService:
    @staticmethod
    def crear_paciente(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def buscar_ci(ci):
        for i in pacientes:
            if i['ci']==ci:
                return i
        return None
    
    @staticmethod
    def buscar_enfermedad(diagnostico):
        n=[]
        for i in pacientes:
            if i['diagnostico']==diagnostico:
                n.append(i)
        return n
    
    @staticmethod
    def buscar_doctor(doctor):
        n=[]
        for i in pacientes:
            if i['doctor']==doctor:
                n.append(i)
        return n
    
    @staticmethod
    def actualizar_paciente(ci,data):
        paciente=PacienteService.buscar_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        return None
    
    @staticmethod
    def eliminar_paciente(ci):
        for i, paciente in enumerate(pacientes):
            if paciente['ci']==ci:
                pacientes.pop(i)
                return pacientes
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
        content_length=int(handler.headers["Content-Length"])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))

class PacienteRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path=="/pacientes/":
            if 'diagnostico' in query_params:
                diagnostico=query_params['diagnostico'][0]
                paciente_diag=PacienteService.buscar_enfermedad(diagnostico)
                if paciente_diag != []:
                    HTTPResponseHandler.response_handler(self,200,paciente_diag)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Diagnostico no encotrado"})
            elif 'doctor' in query_params:
                doctor=query_params['doctor'][0]
                paciente_doc=PacienteService.buscar_doctor(doctor)
                if paciente_doc:
                    HTTPResponseHandler.response_handler(self,200,paciente_doc)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"No existe el doctor"})
            else:
                HTTPResponseHandler.response_handler(self,200,pacientes)
        elif self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            paciente=PacienteService.buscar_ci(ci)
            if paciente:
                HTTPResponseHandler.response_handler(self,200,paciente)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encontrado"})    
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
    def do_POST(self):
        if self.path=="/pacientes":
            data=HTTPResponseHandler.read_data(self)
            paciente=PacienteService.crear_paciente(data)
            HTTPResponseHandler.response_handler(self,201,paciente)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
    
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            paciente_act=PacienteService.actualizar_paciente(ci,data)
            if paciente_act:
                HTTPResponseHandler.response_handler(self,200,paciente_act)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encotrada"})
    
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            paciente_elim=PacienteService.eliminar_paciente(ci)
            if paciente_elim:
                HTTPResponseHandler.response_handler(self,200,paciente_elim)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encontrado"})
        else: 
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encotrada"})
def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,PacienteRequestHandler)
        print(f'Iniciando el servidor en el puerto {port}... ')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Cerrando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
