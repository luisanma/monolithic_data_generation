from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import time
import uuid
import chromadb

# Inicializa la aplicación FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Inicializa el cliente Chroma
chroma_client = chromadb.PersistentClient(path="./vector_database")

# Crear una colección para almacenar respuestas
response_collection = chroma_client.get_or_create_collection(
    name="ollama_responses"
)

# Inicializa el modelo de lenguaje
llm = ChatOllama(
    model="llama3.2:1b",  # gemma2:2b | llama3.2:3b | llama3.2:1b
    temperature=0.5,
    streaming=True
)

# Inicializa el modelo de embeddings
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Define el template del prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu eres un experto en ciberseguridad y redes 5G."),
    ("human", "{input}"),
])


# Modelos de datos
class PromptRequest(BaseModel):
    prompt: str = Field(..., description="El prompt que se enviará al modelo.")
    num_responses: int = Field(
        ge=1, le=100, default=1, description="Número de respuestas a generar."
    )


class ResponseItem(BaseModel):
    id: str
    response: str


class Result(BaseModel):
    responses: list[ResponseItem]


@app.post("/generate-response/", response_model=Result)
async def generate_code(request: PromptRequest):
    user_input = request.prompt.strip()

    if not user_input:
        raise HTTPException(
            status_code=400, detail="El prompt no puede estar vacío."
        )

    try:
        start_time = time.time()

        # Generar múltiples respuestas
        responses = []
        for i in range(request.num_responses):
            # Generar respuesta
            response_content = (prompt | llm).invoke({"input": user_input}).content

            # Generar un ID único
            response_id = str(uuid.uuid4())

            # Calcular embedding
            embedding = embedding_model.embed_query(response_content)

            # Crear ResponseItem
            response_item = ResponseItem(
                id=response_id,
                response=response_content
            )
            responses.append(response_item)

            # Guardar en la base de datos vectorial
            response_collection.add(
                ids=[response_id],
                documents=[response_content],
                embeddings=[embedding]
            )

        elapsed_time = time.time() - start_time
        print(f"Generación completada en {elapsed_time:.6f} segundos para {request.num_responses} respuesta(s).")

        return Result(responses=responses)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar las respuestas: {str(e)}"
        )


@app.get("/all-responses/")
async def get_all_responses():
    try:
        # Recuperar todas las respuestas almacenadas
        results = response_collection.get()

        # Convertir resultados a ResponseItem
        all_responses = [
            ResponseItem(
                id=doc_id, 
                response=doc
            ) 
            for doc_id, doc in zip(results['ids'], results['documents'])
        ]

        return {"responses": all_responses}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al recuperar todas las respuestas: {str(e)}"
        )


@app.get("/search-response/{response_id}")
async def get_response_by_id(response_id: str):
    try:
        # Buscar respuesta por ID
        result = response_collection.get(ids=[response_id])

        if not result['documents']:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        return ResponseItem(
            id=response_id,
            response=result['documents'][0]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al recuperar la respuesta: {str(e)}"
        )
