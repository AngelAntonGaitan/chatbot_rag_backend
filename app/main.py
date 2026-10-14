from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel, Field
from app.rag import rag_core_orchestrator
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_Production_API")

app = FastAPI(
    title="Motor RAG Empresarial API",
    version="1.0.0",
    description="Servicio corporativo de consulta documental inteligente mediante embeddings locales y LLM Cloud."
)


class QueryInput(BaseModel):
    question: str = Field(..., min_length=5, description="Pregunta en lenguaje natural redactada por el usuario",
                          example="¿Cuál es la vigencia del contrato?")
    document_id: str = Field(..., description="Identificador UUID único del documento previamente indexado")


class QueryOutput(BaseModel):
    answer: str = Field(..., description="Respuesta sintetizada e hilada por el modelo de lenguaje")
    document_id: str = Field(..., description="ID del documento analizado")


@app.post("/upload", status_code=status.HTTP_201_CREATED, tags=["Administración Documental"])
async def upload_document(file: UploadFile = File(...)):
    # Validación estricta perimetral de extensiones autorizadas
    if not file.filename.endswith(('.txt', '.pdf')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Archivo inválido. Solo se admiten formatos (.txt) o (.pdf)")

    try:
        raw_bytes = await file.read()
        extracted_text = raw_bytes.decode("utf-8", errors="ignore")

        generated_uuid = str(uuid.uuid4())
        total_chunks = rag_core_orchestrator.process_document_ingestion(generated_uuid, extracted_text)

        logger.info(f"DOCUMENTO INDEXADO: ID={generated_uuid} | Chunks creados={total_chunks}")
        return {
            "document_id": generated_uuid,
            "status": "indexed",
            "chunks_generated": total_chunks
        }
    except Exception as error:
        logger.error(f"FALLO CRÍTICO EN INGESTA: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fallo interno en el pipeline de ingesta: {str(error)}")


@app.post("/ask", response_model=QueryOutput, status_code=status.HTTP_200_OK, tags=["Conversación Semántica"])
def ask_document(payload: QueryInput):
    try:
        ai_response = rag_core_orchestrator.resolve_knowledge_query(payload.document_id, payload.question)
        return QueryOutput(answer=ai_response, document_id=payload.document_id)
    except Exception as error:
        logger.error(f"FALLO EN CONSULTA RAG: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error al procesar la inferencia semántica: {str(error)}")