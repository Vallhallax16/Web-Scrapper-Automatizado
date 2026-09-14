import os
from dotenv import load_dotenv
from pathlib import Path


class Entorno:
    def __init__(self, env_file: str = ".env"):
        self.env_path = Path(env_file)
        self.CargarEnv()

    def CargarEnv(self):
        if self.env_path.exists():
            load_dotenv(dotenv_path=self.env_path)
        else:
            raise FileNotFoundError(f"Archivo de entorno '{self.env_path}' no encontrado.")

    def GetEnv(self, key: str, default: str = None, required: bool = False) -> str:
        value = os.getenv(key, default)
        if required and value is None:
            raise EnvironmentError(f"La variable de entorno '{key}' es obligatoria pero no está definida.")
        return value

    def GetBool(self, key: str, default: bool = False) -> bool:
        val_str = os.getenv(key)
        if val_str is None:
            return default
        return val_str.lower() in ("1", "true", "yes", "on")

    def GetInt(self, key: str, default: int = 0) -> int:
        val_str = os.getenv(key)
        try:
            return int(val_str)
        except (TypeError, ValueError):
            return default