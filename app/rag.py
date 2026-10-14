import os
from openai import OpenAI
from app.embeddings import vector_store_instance

class RAGOrchestrator:
    def __init__(self):
        # Configuración para usar Google AI Studio (compatible con el cliente de OpenAI)
        self.api_key = os.getenv("GEMINI_API_KEY", "mock-key-if-not-present")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/"
        )

    def process_document_ingestion(self, doc_id: str, raw_text: str, chunk_size: int = 400, overlap: int = 50) -> int:
        chunks = []
        start = 0
        while start < len(raw_text):
            end = start + chunk_size
            chunks.append(raw_text[start:end])
            start += (chunk_size - overlap)

        for idx, chunk_text in enumerate(chunks):
            vector_store_instance.add_to_index(doc_id, chunk_text.strip(), idx)

        return len(chunks)

    def resolve_knowledge_query(self, doc_id: str, question: str) -> str:
        relevant_chunks = vector_store_instance.query_similarity(question, doc_id, top_k=2)

        if not relevant_chunks:
            return "Lo lamento, pero no se encontraron evidencias indexadas para el documento solicitado."

        context_evidences = "\n".join([f"[Fragmento {c['chunk_id']}]: {c['text']}" for c in relevant_chunks])

        system_instruction = (
            "Eres un ingeniero experto en análisis de documentos.\n"
            "Responde la pregunta del usuario con total rigor técnico apoyándote EXCLUSIVAMENTE "
            "en el contexto provisto abajo. Si la respuesta no está implícita, admite con honestidad "
            "que la documentación no cuenta con los datos. No inventes absolutos.\n\n"
            f"CONTEXTO DE EVIDENCIAS REALES:\n{context_evidences}"
        )

        response = self.client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": question}
            ],
            temperature=0.0
        )

        return response.choices[0].message.content

rag_core_orchestrator = RAGOrchestrator()