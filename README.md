🌸 Chatbot RAG Empresarial con FastAPI y Gemini
API RESTful desarrollada con FastAPI para realizar consultas documentales inteligentes (Retrieval-Augmented Generation) combinando una base vectorial local y el modelo Google Gemini.

---

🛠️ Tecnologías utilizadas
- Python 3.10
- FastAPI: Framework web moderno y de alto rendimiento.
- Uvicorn: Servidor ASGI para la ejecución de la API.
- Google GenAI (Gemini 3.8-flash via OpenAI Client): Motor de lenguaje de alta precisión.
- Sentence-Transformers & NumPy: Transformación y procesamiento de embeddings semánticos locales.
- Pydantic: Validación de esquemas de datos y contratos de red.

---

🚀 Instalación y ejecución local
1. Clonar el repositorio
git clone https://github.com/AngelAntonGaitan/chatbot_rag_backend.git
cd chatbot_rag_backend

2. Crear y activar el entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar las variables de entorno
export GEMINI_API_KEY="tu-api-key-de-google"  # En Windows: set GEMINI_API_KEY="tu-api-key-de-google"

5. Iniciar el servidor
uvicorn app.main:app --reload

La API estará disponible en http://127.0.0.1:8000.

---

📖 Documentación interactiva
Una vez en ejecución, puedes acceder a la documentación interactiva en:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

📩 Endpoints principales
- POST /upload: Permite la ingesta y fragmentación de documentos corporativos (.txt o .pdf) devolviendo un identificador único.
- POST /ask: Procesa preguntas en lenguaje natural acotadas estrictamente al contenido del documento indexado utilizando evidencias semánticas.

---

Ejemplo de solicitud para consulta (JSON):
{
  "question": "¿Cuál es la política de devoluciones de la empresa?",
  "document_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}

Ejemplo de respuesta:
{
  "answer": "La política de devoluciones permite un reembolso íntegro durante los primeros 30 días posteriores a la compra...",
  "document_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
