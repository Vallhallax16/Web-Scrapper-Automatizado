import os
import re
import zipfile
import win32com.client as win32

class Archivo():
    def __init__(self, ruta = None):
        self.__ruta = os.path.join(os.getcwd(), ruta) if ruta else os.path.join(os.getcwd(), 'Archivos')

        if not os.path.exists(self.__ruta):
            os.makedirs(self.__ruta)

    def getRuta(self):
        return self.__ruta

    def abrirUnArchivo(self,nombreArchivo, codificacion = "utf-8"):
        rutaCompleta = os.path.join(self.__ruta, nombreArchivo)

        with open(rutaCompleta, 'r', encoding = codificacion) as archivo:
            lineasArchivo = archivo.readlines()

        return lineasArchivo

    def escribirArchivo(self, nombreArchivo, contenido, modo = "wb", codificacion = "utf-8"):
        if modo.__contains__("b"):
            with open(os.path.join(self.__ruta, nombreArchivo), modo) as archivo:
                archivo.write(contenido)
        else:
            with open(os.path.join(self.__ruta, nombreArchivo), modo, encoding = codificacion) as archivo:
                archivo.writelines(contenido)

    def obtenerTodos(self,extension):
        patron = rf".*\{extension}$"

        listadoArchivos = [archivo for archivo in os.listdir(self.__ruta)
                           if os.path.isfile(os.path.join(self.__ruta, archivo))
                           and re.match(patron, archivo)]

        return listadoArchivos

    def descomprimirArchivo(self, nombreArchivo):
        with zipfile.ZipFile(
                os.path.join(self.__ruta, nombreArchivo),
                "r"
        ) as zipArchivo:
            archivoCorrupto = zipArchivo.testzip()

            if archivoCorrupto:
                return False
            else:
                zipArchivo.extractall(
                    self.__ruta
                )

        return True

    def ObtenerUltimoArchivo(self):
        listadoArchivos = self.ObtenerRutasArchivos()

        #Destinado para Windows el método getctime
        return max(listadoArchivos, key=os.path.getctime)

    def ObtenerRutasArchivos(self):
        listadoArchivos = [os.path.join(self.__ruta, archivo) for archivo in os.listdir(self.__ruta)
                           if os.path.isfile(os.path.join(self.__ruta, archivo))]

        return listadoArchivos

    def ObtenerNombresArchivos(self):
        listadoArchivos = [archivo for archivo in os.listdir(self.__ruta)
                           if os.path.isfile(os.path.join(self.__ruta, archivo))]

        return listadoArchivos