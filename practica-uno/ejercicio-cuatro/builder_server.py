from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

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

class Paciente:
    def __init__(self):
        self.ci=None
        self.nombre=None
        self.apellido=None
        self.edad=None
        self.genero=None
        self.diagnostico=None
        self.doctor=None
    
    def __str__(self):
        return f"Ci:{self.ci}, Nombre:{self.nombre}, Apellido:{self.apellido}, Edad:{self.edad}, Genero:{self.genero}, Diagnostico:{self.diagnostico},Doctor:{self.doctor}"
                
    
class PacienteBuilder:
    def __init__(self):
        self.paciente=Paciente()
    
    def set_ci(self,ci):
        self.paciente.ci=ci

    def set_nombre(self,nombre):
        self.paciente.nombre=nombre

    def set_apellido(self,apellido):
        self.paciente.apellido=apellido

    def set_edad(self,edad):
        self.paciente.edad=edad

    def set_genero(self,genero):
        self.paciente.genero=genero

    def set_diagnostico(self,diagnostico):
        self.paciente.diagnostico=diagnostico

    def set_doctor(self,doctor):
        self.paciente.doctor=doctor
    
    def get_paciente(self):
        return self.paciente

class PacienteCRE:
    def __init__(self, builder):
        self.builder=builder
    
    def create_paciente(self, ci,nombre,apellido,edad,genero,diagnostico,doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()
    
class PacienteService:
    def __init__(self):
        self.builder=PacienteBuilder()
        self.pacienteCRE=PacienteCRE(self.builder)
    
    def crear_paciente(self,data):
        ci=data.get('ci',None)
        nombre=data['nombre']
        apellido=data.get('apellido',None)
        edad=data.get('edad',None)
        genero=data.get('genero',None)
        diagnostico=data.get('diagnostico',None)
        doctor=data.get('doctor',None)
        paciente=self.pacienteCRE.create_paciente(ci,nombre,apellido,edad,genero,diagnostico,doctor)
        pacientes.append(paciente.__dict__)
        return paciente

    def buscar_ci(self, ci):
        for i in pacientes:
            if i['ci']==ci:
                return i
        return None
    
    def buscar_enfermedad(self,diagnostico):
        n=[]
        for i in pacientes:
            if i['diagnostico']==diagnostico:
                n.append(i)
        return n
    
    def buscar_doctor(self,doctor):
        n=[]
        for i in pacientes:
            if i['doctor']==doctor:
                n.append(i)
        return n
    
    def actualizar_paciente(self,ci,data):
        for paciente in pacientes:
            if paciente['ci']==ci:
                paciente.update(data)
                return pacientes
        return None
    
    def eliminar_paciente(self,ci):
        for i, paciente in enumerate(pacientes):
            if paciente['ci']==ci:
                pacientes.pop(i)
                return pacientes
        return None


class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))
    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class PacienteHandler(BaseHTTPRequestHandler):

    def __init__(self,*args,**kwargs):
        self.controller=PacienteService()
        super().__init__(*args,**kwargs)
    
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path == "/pacientes/":
            if "diagnostico" in query_params:
                diagnostico=query_params['diagnostico'][0]
                paciente_diag=self.controller.buscar_enfermedad(diagnostico)
                if paciente_diag:
                    HTTPResponseHandler.response_handler(self,200,paciente_diag)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Diagnostico no encontrado"})
            elif "doctor" in query_params:
                doctor=query_params['doctor'][0]
                paciente_doc=self.controller.buscar_doctor(doctor)
                if paciente_doc:
                    HTTPResponseHandler.response_handler(self,200,paciente_doc)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"Doctor no encontrado"})
            else:    
                HTTPResponseHandler.response_handler(self,200,pacientes)
        elif parsed_path.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            paciente_ci=self.controller.buscar_ci(ci)
            if paciente_ci:
                HTTPResponseHandler.response_handler(self,200,paciente_ci)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
    
    def do_POST(self):
        if self.path == "/pacientes":
            data=HTTPResponseHandler.read_data(self)
            paciente=self.controller.crear_paciente(data)
            HTTPResponseHandler.response_handler(self,201,paciente.__dict__)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)
            paciente_act=self.controller.actualizar_paciente(ci,data)
            if paciente_act:
                HTTPResponseHandler.response_handler(self,201,paciente_act)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
    
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            paciente_del=self.controller.eliminar_paciente(ci)
            if paciente_del:
                HTTPResponseHandler.response_handler(self,200,paciente_del)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Paciente no encotrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encotrada"})
                

def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,PacienteHandler)
        print(f'Iniciando el servidor en el puerto {port}....')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()
