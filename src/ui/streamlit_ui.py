import streamlit as st
import pandas as pd
from typing import Dict
from agents.llm import Llm
from data.sys_prompts import summarizator, story_teller

class Ui:
    def __init__(self, model):
        self._stories = self.__load_csv()
        self._chapter:int = 1
        self._model:Llm = model
        self._sinopsis = ""


    @property
    def stories(self):
        return self._stories
    @property
    def chapter(self):
        return self._chapter
    @chapter.setter
    def chapter(self,new_chapter)->int:
        self._chapter = new_chapter

    def chapter_add(self):
        self._chapter +=1
    @property
    def model(self):
        return self._model

    def __load_csv(self):
        """
        Carga el archivo CSV de historias fantásticas.

        Returns
        -------
        pd.DataFrame
            El contenido del archivo CSV como un DataFrame.

        Raises
        ------
        FileNotFoundError:
            Si el archivo no existe en la ruta especificada.
        pd.errors.ParserError:
            Si hay un error al interpretar el archivo CSV.
        Exception:
            Para cualquier otro error inesperado.
        """
        try:
            return pd.read_csv("data/historias_fantasticas.csv")
        except FileNotFoundError as e:
            print(f"[Error] Archivo no encontrado: {e}")
        except pd.errors.ParserError as e:
            print(f"[Error] Fallo al analizar el archivo CSV: {e}")
        except Exception as e:
            print(f"[Error] Ocurrió un error inesperado al cargar el archivo: {e}")

    def _extract_row_information(self, story_number: int) -> dict:
        """Extrae un diccionario con título, historia y capítulos como otro diccionario"""
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

    def _create_narration_promtp(self,dict_row_parsed:Dict, summary: str = "")->str:
        """Crea un prompt con la sinopsis"""

        if self.chapter == 1:
            prompt = f"""La sinopsis de la historia es: {dict_row_parsed["sinopsis"]}\n Comienza a explicar el primer capítulo de la historia que es: {dict_row_parsed["chapters"]["cap_1"]}."""
            return prompt
        else:
            prompt = f"""La sinopsis de la historia es: {dict_row_parsed["sinopsis"]}\n El usuario está en el capítulo:{self.chapter}. \n
             Hasta ahora pasaron los siguientes sucesos {summary}.\n
            El siguiente capítulo es el número {self.chapter} y se titula así: {dict_row_parsed["chapters"][f"cap_{self.chapter}"]}.\n Continúa la historia:\n"""
            return prompt



    @staticmethod
    def header () -> None:
        st.markdown("# AI STORIES")
        st.markdown("### by Jorge SB")
                
                    


    @staticmethod
    def explanations():
        st.divider()
        st.markdown("## Sobre el juego")
        st.markdown("""
    Este es un juego de decisiones, es muy simple:

    1. Elige la historia.
    2. El narrador te llevará de la mano a lo largo de 10 capítulos donde tendrás que tomar una decisión en cada uno.
    3. Es posible perder por una decisión o quizá no. No hay vidas, solo decisiones.
    4. Para decidir, pulsa uno de los 2 botones según se te ofrezcan las opciones.
    """)

   
    
    
    def show_stories(self)->None:
        st.divider()
        df = self.stories
        df = df[["id", "titulo", "sinopsis"]]
        st.dataframe(df)

    
    def user_story_selection(self) -> int:
        list_id = self.stories['id'].tolist()

        option = st.selectbox(
            label="Selecciona tu historia:",
            options=list_id
        )
        return option

    def narrate (self, story_number:int, text_response_ai:str = "", user_response:str = "")->str:
        
        self._model.system_prompt=story_teller
        actual_chapter = self.chapter 
        
        dict_row = self._extract_row_information(story_number=story_number)
        if actual_chapter == 1 and text_response_ai == "" and user_response == "":

            response = self._model.generate_response(user_message= self._create_narration_promtp(dict_row_parsed=dict_row, summary=""))
        
        else:
            sinopsis = dict_row["sinopsis"]
            text_response_ai = f"SINOPSIS para que entiendas todo el contexto (No lo repitas, es solo como información, tampoco adelantes acontecimientos): \n {sinopsis}\n{text_response_ai}\n Resume todo esto, la decisión que ha tomado el jugador es la siguiente: "
            resume = self._summarize(text_response_ai=text_response_ai, user_response=user_response)
            response = self._model.generate_response(user_message= self._create_narration_promtp(dict_row_parsed=dict_row, summary=resume))
            
        self.chapter_add()#Le añadimos 1 al capítulo
        return response
            


        
    @staticmethod
    def button_choice()->str:
        st.divider()
        left, right = st.columns(2)
        if left.button(label="A", use_container_width=True):
            return "A"
        if right.button(label = "B", use_container_width=True):
            return "B"
        
    def _summarize(self, text_response_ai:str, user_response:str)->str:
        self._model.system_prompt=summarizator #Ahora le cambié el comportamiento
        message = f"""{text_response_ai}\n El usuario ha tomado el camino: {user_response}\n Explica las consecuencias de su acción y continúa la historia desde este punto."""
        resume = self._model.generate_response(user_message= message)
        return resume



