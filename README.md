# AI Stories: Juego de Rol Interactivo

AI Stories es un juego de rol interactivo basado en texto donde un narrador de IA, impulsado por un modelo de lenguaje local, guía al jugador a través de aventuras de fantasía épica. El jugador toma decisiones que dan forma a la historia, lo que lleva a diferentes resultados, incluido el triunfo o una muerte prematura.

## Características

-   **Narración impulsada por IA:** Un modelo de lenguaje local (LLM) actúa como un maestro del juego, generando la historia en tiempo real.
-   **Historias interactivas:** El jugador elige entre múltiples historias, cada una con su propia sinopsis y capítulos únicos.
-   **Toma de decisiones:** En cada capítulo, el jugador se enfrenta a dos opciones (A o B) que determinan el curso de la narrativa.
-   **Resultados dinámicos:** Las decisiones tienen consecuencias reales, que van desde el éxito y el progreso hasta el fracaso y el "FIN DEL JUEGO".
-   **Interfaz de usuario simple:** Construido con Streamlit para una experiencia de juego limpia y fácil de usar.
-   **Configuración local:** Utiliza Ollama para ejecutar el modelo de lenguaje localmente, asegurando la privacidad y el control.

## Estructura del Proyecto

```
rol_game_agent/
├───.gitignore
├───README.md
├───requirements.txt
├───.git/
├───.venv/
└───src/
    ├───Di_and_Da.py         # Punto de entrada principal de la aplicación
    ├───agents/
    │   └───llm.py           # Clase para interactuar con el modelo de lenguaje (Ollama)
    ├───config/
    │   ├───api_key.py       # (No utilizado actualmente) Gestor de claves de API
    │   └───model.config     # Archivo de configuración para especificar el modelo de Ollama
    ├───data/
    │   ├───historias_fantasticas.csv  # Datos de la historia (títulos, sinopsis, capítulos)
    │   └───sys_prompts.py   # Prompts del sistema para guiar el comportamiento de la IA
    └───ui/
        └───streamlit_ui.py  # Lógica de la interfaz de usuario de Streamlit
```

## Cómo Funciona

El juego utiliza una combinación de componentes para crear una experiencia de narración dinámica:

-   **`Di_and_Da.py`**: Este es el script principal que se ejecuta. Inicializa la interfaz de usuario de Streamlit, el modelo de lenguaje (`Llm`) y gestiona el estado de la sesión del juego (como la historia actual, el número de capítulo y las elecciones del usuario). Orquesta el flujo del juego, comenzando la historia y generando nuevos capítulos basados en la entrada del jugador.

-   **`ui/streamlit_ui.py`**: La clase `Ui` es responsable de renderizar todos los elementos de la interfaz de usuario. Carga las historias desde el archivo CSV, las muestra en un DataFrame, maneja la selección de historias del usuario y muestra los botones de decisión. También formatea los prompts que se envían al LLM.

-   **`agents/llm.py`**: La clase `Llm` encapsula la interacción con el LLM a través de la API compatible con OpenAI de Ollama. Lee el nombre del modelo desde `src/config/model.config`, formatea los mensajes y envía solicitudes al LLM para generar el texto de la historia.

-   **`data/historias_fantasticas.csv`**: Este archivo CSV contiene la estructura de cada aventura. Cada fila representa una historia con un ID, título, sinopsis y los títulos de sus 10 capítulos. Esta información se utiliza para guiar al narrador de la IA.

-   **`data/sys_prompts.py`**: Este archivo define los "prompts del sistema" que dan al LLM su personalidad y directrices. `story_teller` instruye a la IA para que actúe como un maestro del juego de fantasía, mientras que `summarizator` se utiliza para resumir el progreso de la historia entre capítulos, asegurando la continuidad.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd rol_game_agent
```

### 2. Instalar Dependencias de Python

Se recomienda crear un entorno virtual.

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`
```

Instala los paquetes necesarios desde `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Instalar y Configurar Ollama

El juego requiere que Ollama se ejecute localmente para servir el modelo de lenguaje.

-   **Descargar Ollama:** Ve al [sitio web de Ollama](https://ollama.com/) y descarga la aplicación para tu sistema operativo.

-   **Iniciar el Servidor de Ollama:** Una vez instalado, ejecuta el siguiente comando en una terminal separada para iniciar el servidor de Ollama. Debes mantener esta terminal abierta mientras juegas.

    ```bash
    ollama serve
    ```

-   **Descargar el Modelo de Lenguaje:** El modelo recomendado se especifica en `src/config/model.config`. Usa el siguiente comando para descargarlo.

    ```bash
    ollama pull gemma3n:e4b
    ```

## Uso

Con el servidor de Ollama ejecutándose en una terminal, abre una nueva terminal, navega al directorio del proyecto y ejecuta la aplicación Streamlit.

Asegúrate de que tu entorno virtual esté activado.

```bash
streamlit run src/Di_and_Da.py
```

La aplicación debería abrirse en tu navegador web. ¡Ahora puedes seleccionar una historia y comenzar tu aventura!