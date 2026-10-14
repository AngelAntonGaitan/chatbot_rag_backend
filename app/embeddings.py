import os
import numpy as np
from sentence_transformers import SentenceTransformer


class LocalVectorStore:
    def __init__(self):
        # Inicialización del modelo transformador de sentencias (384 dimensiones)
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        # Estructuras de almacenamiento en memoria simulando persistencia indexada
        self.vectors = []  # Lista de arrays numpy
        self.documents = []  # Lista de dicts con {'id', 'text', 'metadata'}

    def generate_vector(self, text: str) -> list:
        embedding = self.encoder.encode(text)
        return embedding.tolist()

    def add_to_index(self, doc_id: str, text_chunk: str, chunk_index: int):
        vector = self.generate_vector(text_chunk)
        self.vectors.append(vector)
        self.documents.append({
            "document_id": doc_id,
            "chunk_id": chunk_index,
            "text": text_chunk
        })

    def query_similarity(self, query_text: str, doc_id: str, top_k: int = 2) -> list:
        if not self.vectors:
            return []

        query_vector = np.array(self.generate_vector(query_text))
        results = []

        # Búsqueda semántica lineal filtrada por identificador de documento
        for idx, vec in enumerate(self.vectors):
            if self.documents[idx]["document_id"] != doc_id:
                continue

            target_vector = np.array(vec)
            # Cómputo matemático de la similitud coseno
            dot_product = np.dot(query_vector, target_vector)
            norm_q = np.linalg.norm(query_vector)
            norm_t = np.linalg.norm(target_vector)

            similarity = float(dot_product / (norm_q * norm_t)) if norm_q > 0 and norm_t > 0 else 0.0
            results.append((similarity, self.documents[idx]))

        # Ordenación descendente por score de similitud semántica
        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results[:top_k]]


vector_store_instance = LocalVectorStore()