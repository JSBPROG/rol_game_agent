from dotenv import load_dotenv
import os
import getpass

class OpenAIKeyManager:
    def __init__(self):
        self.key_name = "OPENAI_API_KEY"

    def load_dotenv_file(self):
        try:
            load_dotenv()
        except Exception as e:
            print(f"Error cargando .env: {e}")

    def get_key(self) -> str:
        key = os.getenv(self.key_name)
        if key:
            print("Clave OpenAI existe y se cargó correctamente!")
        return key

    def prompt_key(self) -> str:
        try:
            key = getpass.getpass(f"Ingrese {self.key_name}: ")
            if not key:
                print("No se ingresó clave.")
                return ""
            return key
        except Exception as e:
            print(f"Error solicitando clave: {e}")
            return ""

    def save_key(self, key: str):
        os.environ[self.key_name] = key
        print("Clave guardada en variables de entorno para esta sesión.")

    def get_or_prompt_key(self) -> str:
        self.load_dotenv_file()
        key = self.get_key()
        if key:
            return key
        print(f"La clave {self.key_name} no está definida en .env, por favor ingrésala:")
        key = self.prompt_key()
        if key:
            self.save_key(key)
        return key


if __name__ == "__main__":
    pass
    #Ejemplo de uso
    """key_manager = OpenAIKeyManager()
    api_key = key_manager.get_or_prompt_key()
    print("Clave obtenida:", api_key)"""
