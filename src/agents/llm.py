from IPython.display import display, Markdown
from typing import List, Dict
from openai import OpenAI
from configparser import ConfigParser, NoSectionError, NoOptionError
import os

class Llm:
    """
    Clase que representa un modelo de lenguaje de OpenAI, proporcionando métodos para interactuar
    con el modelo, generar respuestas y visualizar los resultados.

    Atributos:
        model (str): El nombre del modelo de OpenAI a utilizar.
        url (str): La URL base de la API de OpenAI.
        api_key (str): La clave de API para autenticar las solicitudes a OpenAI.
        system_prompt (str): El mensaje de sistema opcional que orienta el comportamiento del modelo.
    """

    def __init__(self, url: str, api_key: str, system_prompt: str = ""):
        """
        Inicializa la clase con los parámetros proporcionados.

        Parámetros:
            model (str): El nombre del modelo de OpenAI a utilizar.
            url (str): La URL base de la API de OpenAI.
            api_key (str): La clave de API para autenticar las solicitudes a OpenAI.
            system_prompt (str, opcional): El mensaje de sistema que orienta el modelo (por defecto es una cadena vacía).
        """
        self._model = self._set_model()
        self._url = url
        self._api_key = api_key
        self._system_prompt = system_prompt
        self._client = self._load_openai()

    @property
    def model(self) -> str:
        """
        Obtiene el modelo actual.

        Retorna:
            str: El modelo actual configurado para la instancia.
        """
        return self._model

    @model.setter
    def model(self, value: str):
        """
        Establece un nuevo modelo para la instancia.

        Parámetros:
            value (str): El nombre del nuevo modelo a utilizar.
        """
        self._model = value

    @property
    def url(self) -> str:
        """
        Obtiene la URL base de la API.

        Retorna:
            str: La URL configurada para la instancia.
        """
        return self._url

    @url.setter
    def url(self, value: str):
        """
        Establece una nueva URL base para la API.

        Parámetros:
            value (str): La nueva URL base para la API.
        """
        self._url = value
        self._client = self._load_openai()

    @property
    def system_prompt(self) -> str:
        """
        Obtiene el mensaje de sistema actual.

        Retorna:
            str: El mensaje de sistema configurado.
        """
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, new_sys_prompt: str):
        """
        Establece un nuevo mensaje de sistema.

        Parámetros:
            new_sys_prompt (str): El nuevo mensaje de sistema.
        """
        self._system_prompt = new_sys_prompt

    def _load_openai(self) -> OpenAI:
        """
        Carga e inicializa el cliente de OpenAI utilizando la URL base y la clave de API proporcionadas.

        Retorna:
            OpenAI: Una instancia del cliente de la API de OpenAI.
        """
        return OpenAI(base_url=self._url, api_key=self._api_key)
    
    def _set_model(self) -> str:
        """
        Lee el modelo desde el archivo de configuración y lo retorna.
        
        Returns
        -------
        str
            Nombre del modelo especificado en el archivo de configuración.

        Raises
        ------
        FileNotFoundError:
            Si el archivo de configuración no existe.
        NoSectionError:
            Si la sección "Model" no está en el archivo.
        NoOptionError:
            Si la opción "name" no está en la sección "Model".
        """
        try:
            config = ConfigParser()

            if not os.path.exists("config/model.config"):
                raise FileNotFoundError("El archivo 'config/model.config' no existe.")

            config.read("config/model.config")

            return config.get("Model", "name")

        except FileNotFoundError as e:
            print(f"[Error] Archivo no encontrado: {e}")
        except NoSectionError as e:
            print(f"[Error] Sección faltante en el archivo de configuración: {e}")
        except NoOptionError as e:
            print(f"[Error] Clave faltante en la sección del archivo de configuración: {e}")
        except Exception as e:
            print(f"[Error] Error inesperado: {e}")

    def _format_message(self, user_message: str) -> List[Dict[str, str]]:
        """
        Formatea un mensaje del usuario en el formato requerido por la API de OpenAI.

        Parámetros:
            user_message (str): El mensaje enviado por el usuario.

        Retorna:
            List[Dict[str, str]]: Una lista de diccionarios con el formato adecuado para la API.
        """
        return [{"role": "user", "content": user_message}]

    def _format_sys_prompt(self) -> List[Dict[str, str]]:
        """
        Formatea el mensaje de sistema en el formato requerido por la API de OpenAI.

        Retorna:
            List[Dict[str, str]]: Una lista de diccionarios con el mensaje de sistema formateado.
        """
        return [{"role": "system", "content": self._system_prompt}]

    def generate_response(self, user_message: str) -> str:
        """
        Genera una respuesta del modelo de OpenAI basándose en el mensaje del usuario y el mensaje de sistema (si se proporciona).

        Parámetros:
            user_message (str): El mensaje enviado por el usuario.

        Retorna:
            str: La respuesta generada por el modelo.
        """
        if not self._system_prompt:
            messages = self._format_message(user_message)
        else:
            messages = self._format_sys_prompt() + self._format_message(user_message)
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        return response.choices[0].message.content

    def chat(self, message, history):
        """
        Envía un mensaje al modelo, incluyendo el historial de mensajes anteriores, y devuelve la respuesta.

        Parámetros:
            message (str): El mensaje que el usuario desea enviar al modelo.
            history (List[Dict[str, str]]): El historial de mensajes previos entre el usuario y el modelo.

        Retorna:
            str: La respuesta generada por el modelo.
        """
        messages = self._format_sys_prompt() + history + self._format_message(message)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        return response.choices[0].message.content

    def visualize_response(self, response: str) -> None:
        """
        Muestra la respuesta generada por el modelo en un formato Markdown en la interfaz de usuario.

        Parámetros:
            response (str): La respuesta generada por el modelo que se desea visualizar.
        """
        display(Markdown(response))