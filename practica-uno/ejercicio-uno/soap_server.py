from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler
def sumar(a,b):
    return f'la suma es {a+b}'

def multiplicar(a,b):
    return f'la multiplicacion es {a*b}'

def restar(a,b):
    return f'la resta es {a-b}'

def dividir(a,b):
    return f'la division es {a/b}'

dispatcher=SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Suma",
    sumar,
    returns={"sumar": str},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Multiplicacion",
    multiplicar,
    returns={"multiplicar": str},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Resta",
    restar,
    returns={"restar": str},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Division",
    dividir,
    returns={"dividir": str},
    args={"a": int, "b": int},
)

server=HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher=dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()

