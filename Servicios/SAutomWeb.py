from Infraestructura import IArchivo
from Infraestructura import IDescarga

class AutomWeb:
    def __init__(self, nomArch = "CP_comprimido.zip"):
        self.__nomArch = nomArch

    def iniciarWS(self, dicHeaders, url, arrCampos, dicActualizacion = None):
        descargar = IDescarga.Descargador()

        descargar.setHeaders(dicHeaders)
        descargar.setPayload(url, arrCampos)
        archDescar = descargar.descargarArchivo(dicActualizacion)

        archivos = IArchivo.Archivo()
        archivos.escribirArchivo(self.__nomArch, archDescar, modo = "wb")