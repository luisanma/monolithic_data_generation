# Solución Monolítica de IA Generativa basada en Langchain y Ollama

Esta es una solución monolítica de generación de respuestas utilizando inteligencia artificial, que emplea Langchain y Ollama en su versión apificada mediante FastAPI. Está diseñada para generar múltiples respuestas basadas en un prompt dado y almacenar las respuestas en una base de datos vectorial para aplicar RAG posteriormente.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```tree
monolithic_data_generation/
│
├── app_event.py            # Main application logic
├── index.html              # Web interface
├── utils.py                # Utility functions
├── langollama-simple.ipynb # Jupyter notebook for exploration
└── requirements.txt        # Project dependencies
```tree

## Instrucciones para Ejecutar el Servicio

### Requisitos Previos

1. **Instalar Conda**:
   Si aún no tienes Conda, instálalo desde [aquí](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

2. **Crear y Activar el Entorno Conda**:
   Crea un nuevo entorno con Python 3.10 y actívalo:

   ```bash
   conda create -n new_env python=3.10
   conda activate new_env

3. **Clonar el Repositorio**:
   Utiliza git para clonar el proyecto:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd monolithic_data_generation

4. **Instalar Deopendencias**:
   Utiliza git para clonar el proyecto:

   ```bash
   pip install -r requirements.txt

5. **Ejecutar el servicio**:
   Para iniciar el servidor, ejecuta el siguiente comando:

   ```bash
   uvicorn app_event:app --reload
   
## Endpoints

### Generar Respuestas

**POST /generate-response/**

Genera múltiples respuestas de IA basadas en el prompt de entrada.

**Parámetros:**

- `prompt`: Texto de entrada para la generación de respuestas.
- `num_responses`: Número de respuestas a generar (1-100).

---

### Recuperar Respuestas

**GET /all-responses/**

Recupera todas las respuestas generadas por IA almacenadas.

---

### Buscar Respuesta Específica

**GET /search-response/{response_id}**

Recupera una respuesta específica por su ID único.
