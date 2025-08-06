import streamlit as st
import pandas as pd
from typing import Dict
from agents.llm import Llm
from data.sys_prompts import summarizator, story_teller

class Ui:
    """
    Gestiona la interfaz de usuario de la aplicación de historias interactivas.

    Esta clase es responsable de cargar los datos de las historias, renderizar
    los componentes de la interfaz de usuario con Streamlit y manejar la lógica
    de interacción con el usuario.

    Atributos
    ----------
    stories : pd.DataFrame
        DataFrame con las historias cargadas desde el archivo CSV.
    chapter : int
        Número del capítulo actual en la historia.
    model : Llm
        Instancia de la clase Llm para interactuar con el modelo de lenguaje.
    """

    def __init__(self, model: Llm):
        """
        Inicializa la clase Ui.

        Parámetros
        ----------
        model : Llm
            Instancia de la clase Llm para la generación de texto.
        """
        self.__stories = self.__load_csv()
        self.__chapter: int = 1
        self.__model: Llm = model

    @property
    def stories(self) -> pd.DataFrame:
        """
        pd.DataFrame: Obtiene el DataFrame con las historias.
        """
        return self.__stories

    @property
    def chapter(self) -> int:
        """
        int: Obtiene o establece el número del capítulo actual.
        """
        return self.__chapter

    @chapter.setter
    def chapter(self, new_chapter: int) -> None:
        self.__chapter = new_chapter

    def chapter_add(self) -> None:
        """
        Incrementa el contador de capítulos en uno.
        """
        self.__chapter += 1

    @property
    def model(self) -> Llm:
        """
        Llm: Obtiene la instancia del modelo de lenguaje.
        """
        return self.__model

    def __load_csv(self) -> pd.DataFrame:
        """
        Carga las historias desde un archivo CSV.

        Retorna
        -------
        pd.DataFrame
            DataFrame con los datos de las historias.

        Raises
        ------
        FileNotFoundError
            Si el archivo 'data/historias_fantasticas.csv' no se encuentra.
        pd.errors.ParserError
            Si ocurre un error al parsear el archivo CSV.
        """
        try:
            return pd.read_csv("data/historias_fantasticas.csv")
        except FileNotFoundError as e:
            print(f"[Error] Archivo no encontrado: {e}")
            raise
        except pd.errors.ParserError as e:
            print(f"[Error] Fallo al analizar el archivo CSV: {e}")
            raise

    def __extract_row_information(self, story_number: int) -> Dict:
        """
        Extrae la información de una historia específica del DataFrame.

        Parámetros
        ----------
        story_number : int
            ID de la historia a extraer.

        Retorna
        -------
        Dict
            Diccionario con el título, sinopsis y capítulos de la historia.
        """
        row = self.stories[self.stories["id"] == story_number]
        if row.empty:
            return {}

        fila = row.iloc[0]

        dict_return = {
            "id": fila["id"],
            "titulo": fila["titulo"],
            "sinopsis": fila["sinopsis"],
        }

        chapters_cols = [col for col in self.stories.columns if col.startswith("cap_")]
        dict_return["chapters"] = fila[chapters_cols].to_dict()

        return dict_return

    def __create_narration_promtp(self, dict_row_parsed: Dict, summary: str = "") -> str:
        """
        Crea el prompt de narración para el modelo de lenguaje.

        Parámetros
        ----------
        dict_row_parsed : Dict
            Diccionario con la información de la historia.
        summary : str, opcional
            Resumen de los eventos previos de la historia. Por defecto es "".

        Retorna
        -------
        str
            Prompt formateado para la generación de la narración.
        """
        if self.chapter == 1:
            prompt = f'''La sinopsis de la historia es: {dict_row_parsed["sinopsis"]}\n Comienza a explicar el primer capítulo de la historia que es: {dict_row_parsed["chapters"]["cap_1"]}.'''
            return prompt
        else:
            prompt = f'''La sinopsis de la historia es: {dict_row_parsed["sinopsis"]}\n El usuario está en el capítulo:{self.chapter}. \n\n             Hasta ahora pasaron los siguientes sucesos {summary}.\n\n            El siguiente capítulo es el número {self.chapter} y se titula así: {dict_row_parsed["chapters"][f"cap_{self.chapter}"]}.\n Tienes que empezar así: \nExplicas lo que ocurrió por la decisión del usuario.Enlazas esto con el nuevo capítulo, lo explicas y llegas a la nueva pregunta.:\n'''
            return prompt

    @staticmethod
    def header() -> None:
        """
        Muestra el encabezado de la aplicación en Streamlit.
        """
        st.markdown("# AI STORIES")
        st.markdown("### by Jorge SB")

    @staticmethod
    def explanations() -> None:
        """
        Muestra las explicaciones sobre cómo jugar.
        """
        st.divider()
        st.markdown("## Sobre el juego")
        st.markdown("""
    Este es un juego de decisiones, es muy simple:

    1. Elige la historia.
    2. El narrador te llevará de la mano a lo largo de 10 capítulos donde tendrás que tomar una decisión en cada uno.
    3. Es posible perder por una decisión o quizá no. No hay vidas, solo decisiones.
    4. Para decidir, pulsa uno de los 2 botones según se te ofrezcan las opciones.
    """)

    def show_stories(self) -> None:
        """
        Muestra la lista de historias disponibles en un DataFrame de Streamlit.
        """
        st.divider()
        df = self.stories
        df = df[["id", "titulo", "sinopsis"]]
        st.dataframe(df)

    def user_story_selection(self) -> int:
        """
        Muestra un selector para que el usuario elija una historia.

        Retorna
        -------
        int
            ID de la historia seleccionada por el usuario.
        """
        list_id = self.stories['id'].tolist()

        option = st.selectbox(
            label="Selecciona tu historia:",
            options=list_id
        )
        return option

    def narrate(self, story_number: int, text_response_ai: str = "", user_response: str = "") -> str:
        """
        Genera el siguiente capítulo de la historia utilizando el modelo de lenguaje.

        Parámetros
        ----------
        story_number : int
            ID de la historia que se está narrando.
        text_response_ai : str, opcional
            Texto del capítulo anterior generado por la IA. Por defecto es "".
        user_response : str, opcional
            Elección del usuario en el capítulo anterior. Por defecto es "".

        Retorna
        -------
        str
            Texto del nuevo capítulo generado por el modelo.
        """
        self.__model.system_prompt = story_teller
        actual_chapter = self.chapter

        dict_row = self.__extract_row_information(story_number=story_number)
        if actual_chapter == 1 and text_response_ai == "" and user_response == "":
            response = self.__model.generate_response(user_message=self.__create_narration_promtp(dict_row_parsed=dict_row, summary=""))
        else:
            sinopsis = dict_row["sinopsis"]
            text_response_ai = f'SINOPSIS para que entiendas todo el contexto (No lo repitas, es solo como información, tampoco adelantes acontecimientos): \n {sinopsis}\n{text_response_ai}\n Resume todo esto, la decisión que ha tomado el jugador es la siguiente: '
            resume = self.__summarize(text_response_ai=text_response_ai, user_response=user_response)
            self.__model.system_prompt = story_teller
            response = self.__model.generate_response(user_message=self.__create_narration_promtp(dict_row_parsed=dict_row, summary=resume))

        self.chapter_add()  # Le añadimos 1 al capítulo
        return response

    @staticmethod
    def button_choice() -> str:
        """
        Muestra los botones de elección (A y B) y retorna la opción seleccionada.

        Retorna
        -------
        str
            'A' o 'B' según el botón que presione el usuario.
        """
        st.divider()
        left, right = st.columns(2)
        if left.button(label="A", use_container_width=True):
            return "A"
        if right.button(label="B", use_container_width=True):
            return "B"

    def __summarize(self, text_response_ai: str, user_response: str) -> str:
        """
        Resume el estado actual de la historia para mantener la continuidad.

        Parámetros
        ----------
        text_response_ai : str
            Texto del capítulo anterior generado por la IA.
        user_response : str
            Elección del usuario en el capítulo anterior.

        Retorna
        -------
        str
            Resumen de la historia hasta el momento.
        """
        self.__model.system_prompt = summarizator  # Ahora le cambié el comportamiento
        message = f'''{text_response_ai}\n El usuario ha tomado el camino: {user_response}\n Explica las consecuencias de su acción y continúa la historia desde este punto.'''
        resume = self.__model.generate_response(user_message=message)
        return resume
