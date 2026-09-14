import requests

from bs4 import BeautifulSoup

class Descargador:
    def __init__(self):
        self.__sesion   = requests.Session()
        self.__payload  = {}
        self.__url      = str()

    def setHeaders(self, dicHeaders):
        self.__sesion.headers.update(dicHeaders)

    def setPayload(self, url, arrCampos, timeout = 60):
        self.__url = url

        respuesta = self.__sesion.get(
            url,
            timeout = timeout
        )

        respuesta.raise_for_status()

        pagina = BeautifulSoup(
            respuesta.text,
            "html.parser"
        )

        self.__payload = {}

        for campo in arrCampos:
            elemento = pagina.find(
                "input",
                {"name": campo}
            )

            self.__payload[campo] = (
                elemento.get("value", "")
                if elemento
                else ""
            )

    def descargarArchivo(self, dicActualizacion = None, timeout = 120):
        if dicActualizacion != None:
            self.__payload.update(dicActualizacion)

        respuesta = self.__sesion.post(
            self.__url,
            data    = self.__payload,
            timeout = timeout
        )

        respuesta.raise_for_status()

        return respuesta.content