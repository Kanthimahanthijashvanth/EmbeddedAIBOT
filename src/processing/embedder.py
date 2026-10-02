from langchain_huggingface import HuggingFaceEmbeddings


class WorkshopEmbedder:

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model_name = model_name

        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name
        )

    def embed_documents(self, documents):

        texts = [
            document.page_content
            for document in documents
        ]

        vectors = self.embeddings.embed_documents(
            texts
        )

        return vectors

    def embed_query(self, query):

        return self.embeddings.embed_query(
            query
        )