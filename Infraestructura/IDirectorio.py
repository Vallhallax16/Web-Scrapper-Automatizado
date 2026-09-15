import os
import shutil

class Directorio:
    def borrarCarpeta(self, ruta):
        if not os.path.exists(ruta):
            return False

        if not os.path.isdir(ruta):
            raise NotADirectoryError(
                f"La ruta no corresponde a una carpeta: {ruta}"
            )

        shutil.rmtree(ruta)

        return True