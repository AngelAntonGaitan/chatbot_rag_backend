# 🌸 Chatbot RAG Backend con FastAPI

API RESTful desarrollada con **FastAPI** para realizar consultas documentales inteligentes (Retrieval-Augmented Generation) combinando una base vectorial local y el modelo **Google Gemini**.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10**
- **FastAPI**: Framework web moderno y de alto rendimiento.
- **Uvicorn**: Servidor ASGI para la ejecución de la API.
- **Google GenAI (Gemini 3.8-flash)**: Motor de lenguaje avanzado mediante la interfaz compatible con OpenAI.
- **Sentence-Transformers & NumPy**: Transformación, indexación y búsqueda semántica de vectores locales.
- **Pydantic**: Validación y tipado robusto de esquemas de datos.

---

## 🚀 Instalación y ejecución local

### 1. Clonar el repositorio
```bash
git clone https://github.com/AngelAntonGaitan/chatbot_rag_backend.git
cd chatbot_rag_backend
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
```bash
export GEMINI_API_KEY="tu-api-key-de-google"  # En Windows: set GEMINI_API_KEY="tu-api-key-de-google"
```

### 5. Iniciar el servidor
```bash
uvicorn app.main:app --reload
```
La API estará disponible en http://127.0.0.1:8000.

---

## 📖 Documentación interactiva
Una vez en ejecución, puedes acceder a la documentación interactiva en:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📩 Endpoints principales

### - POST /upload
Permite la subida e indexación de archivos corporativos en formato `.txt` o `.pdf`.

### - POST /ask
Procesa consultas conversacionales basadas estrictamente en las evidencias del documento analizado.

Ejemplo de solicitud (JSON):
```json
{
  "question": "¿Cuál es la política de devoluciones de la empresa?",
  "document_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

Ejemplo de respuesta:
```json
{
  "answer": "La política de devoluciones permite un reembolso íntegro durante los primeros 30 días...",
  "document_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```
