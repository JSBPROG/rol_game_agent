from IPython.display import display, Markdown
from typing import List, Dict
from openai import OpenAI
from configparser import ConfigParser, NoSectionError, NoOptionError
import os

class Llm:
    """
    Clase que representa un modelo de lenguaje de OpenAI.

    Esta clase proporciona métodos para interactuar con un modelo de lenguaje
    de OpenAI, permitiendo generar respuestas y visualizar los resultados.

    Atributos
    ----------
    model : str
        Nombre del modelo de OpenAI a utilizar.
    url : str
        URL base de la API de OpenAI.
    api_key : str
        Clave de API para autenticar las solicitudes a OpenAI.
    system_prompt : str
        Mensaje de sistema opcional para orientar el comportamiento del modelo.
    """

    def __init__(self, url: str, api_key: str, system_prompt: str = ""):
        """
        Inicializa la clase Llm.

        Parámetros
        ----------
        url : str
            URL base de la API de OpenAI.
        api_key : str
            Clave de API para autenticar las solicitudes a OpenAI.
        system_prompt : str, opcional
            Mensaje de sistema para orientar el modelo. Por defecto es "".
        """
        self.__model = self.__set_model()
        self.__url = url
        self.__api_key = api_key
        self.__system_prompt = system_prompt
        self.__client = self.__load_openai()

    @property
    def model(self) -> str:
        """
        str: Obtiene o establece el modelo de OpenAI a utilizar.
        """
        return self.__model

    @model.setter
    def model(self, value: str):
        self.__model = value

    @property
    def url(self) -> str:
        """
        str: Obtiene o establece la URL base de la API de OpenAI.
        """
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value
        self.__client = self.__load_openai()

    @property
    def system_prompt(self) -> str:
        """
        str: Obtiene o establece el mensaje de sistema.
        """
        return self.__system_prompt

    @system_prompt.setter
    def system_prompt(self, new_sys_prompt: str):
        self.__system_prompt = new_sys_prompt

    def __load_openai(self) -> OpenAI:
        """
        Carga e inicializa el cliente de OpenAI.

        Retorna
        -------
        OpenAI
            Instancia del cliente de la API de OpenAI.
        """
        return OpenAI(base_url=self.__url, api_key=self.__api_key)

    def __set_model(self) -> str:
        """
        Lee el modelo desde el archivo de configuración.

        Retorna
        -------
        str
            Nombre del modelo especificado en el archivo de configuración.

        Raises
        ------
        FileNotFoundError
            Si el archivo 'config/model.config' no existe.
        NoSectionError
            Si la sección 'Model' no se encuentra en el archivo.
        NoOptionError
            Si la opción 'name' no se encuentra en la sección 'Model'.
        """
        try:
            config = ConfigParser()
            config_path = "src/config/model.config"
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"El archivo '{config_path}' no existe.")
            config.read(config_path)
            return config.get("Model", "name")
        except (FileNotFoundError, NoSectionError, NoOptionError) as e:
            print(f"[Error] {e}")
            raise

    def __format_message(self, user_message: str) -> List[Dict[str, str]]:
        """
        Formatea un mensaje de usuario para la API de OpenAI.

        Parámetros
        ----------
        user_message : str
            Mensaje del usuario.

        Retorna
        -------
        List[Dict[str, str]]
            Lista de diccionarios con el mensaje formateado.
        """
        return [{"role": "user", "content": user_message}]

    def __format_sys_prompt(self) -> List[Dict[str, str]]:
        """
        Formatea el mensaje de sistema para la API de OpenAI.

        Retorna
        -------
        List[Dict[str, str]]
            Lista de diccionarios con el mensaje de sistema formateado.
        """
        return [{"role": "system", "content": self.__system_prompt}]

    def generate_response(self, user_message: str) -> str:
        """
        Genera una respuesta del modelo de OpenAI.

        Parámetros
        ----------
        user_message : str
            Mensaje del usuario.

        Retorna
        -------
        str
            Respuesta generada por el modelo.
        """
        if not self.__system_prompt:
            messages = self.__format_message(user_message)
        else:
            messages = self.__format_sys_prompt() + self.__format_message(user_message)
        
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages
        )
        return response.choices[0].message.content

    def chat(self, message: str, history: List[Dict[str, str]]):
        """
        Envía un mensaje al modelo, incluyendo el historial de chat.

        Parámetros
        ----------
        message : str
            Mensaje del usuario.
        history : List[Dict[str, str]]
            Historial de mensajes previos.

        Retorna
        -------
        str
            Respuesta generada por el modelo.
        """
        messages = self.__format_sys_prompt() + history + self.__format_message(message)
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages
        )
        return response.choices[0].message.content

    def visualize_response(self, response: str) -> None:
        """
        Muestra la respuesta del modelo en formato Markdown.

        Parámetros
        ----------
        response : str
            Respuesta generada por el modelo.
        """
        display(Markdown(response))
