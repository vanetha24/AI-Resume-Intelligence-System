from sentence_transformers import SentenceTransformer


MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


class EmbeddingModel:

    def __init__(self):

        print(
            "Loading Sentence Transformer model..."
        )

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    def encode(self, text):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )