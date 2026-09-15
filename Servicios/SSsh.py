import os
import paramiko

from Infraestructura import IEntorno

class Ssh:
    def __init__(self):
        self.__getEnvValores()

    def __getEnvValores(self):
        archEnv = IEntorno.Entorno()

        self.__host = archEnv.GetEnv("HOST")
        self.__puerto = int(archEnv.GetEnv("PUERTO"))
        self.__usuario = archEnv.GetEnv("USUARIO")
        self.__contra = archEnv.GetEnv("CONTRASENA")
        self.__dirSAS = archEnv.GetEnv("DIR_SAS")
        self.__bash = archEnv.GetEnv("BASH_EJECUTABLE")

    def iniciarCarga(self, rutaArchSubir):
        self.__conectar()
        resultado = self.__subirArchivo(rutaArchSubir)
        self.__desconectar()

        if resultado:
            print("Carga exitosa al servidor")
        else:
            print("Carga fallida al servidor")

    def ejecutarBash(self):
        self.__conectar()

        try:
            stdin, stdout, stderr = self.__cliente.exec_command(
                self.__bash
            )

            codigoSalida = stdout.channel.recv_exit_status()

            salida = stdout.read().decode(
                "utf-8",
                errors="replace"
            )

            error = stderr.read().decode(
                "utf-8",
                errors="replace"
            )

            if codigoSalida != 0:
                raise RuntimeError(
                    f"El comando remoto terminó con código "
                    f"{codigoSalida}.\n\n"
                    f"STDOUT:\n{salida}\n\n"
                    f"STDERR:\n{error}"
                )

            return salida

        finally:
            self.__desconectar()

    def __conectar(self):
        self.__cliente = paramiko.SSHClient()

        rutaKnownHosts = os.path.expanduser(
            "~/.ssh/known_hosts"
        )

        self.__cliente.load_host_keys(
            rutaKnownHosts
        )

        self.__cliente.connect(
            hostname=self.__host,
            port=self.__puerto,
            username=self.__usuario,
            password=self.__contra
        )

    def __desconectar(self):
        if self.__cliente:
            self.__cliente.close()
            self.__cliente = None

    def __subirArchivo(self, rutaLocal):
        if not os.path.isfile(rutaLocal):
            raise FileNotFoundError(
                f"No existe el archivo local: {rutaLocal}"
            )
        else:
            arrRuta = rutaLocal.split("\\")
            rutaRemota = self.__dirSAS + arrRuta[-1]

            with self.__cliente.open_sftp() as sftp:
                sftp.put(
                    rutaLocal,
                    rutaRemota,
                )

                resultado = self.__validarCarga(rutaLocal, rutaRemota, sftp)

        return resultado

    def __validarCarga(self, rutaLocal, rutaRemota, sftp):
        tamanioLocal = os.path.getsize(
            rutaLocal
        )

        tamanioRemoto = sftp.stat(
            rutaRemota
        ).st_size

        if tamanioLocal != tamanioRemoto:
            raise IOError(
                "El tamaño del archivo remoto "
                "no coincide con el archivo local. "
                f"Local {tamanioLocal} vs Remoto {tamanioRemoto}"
            )

            return False
        else:
            return True