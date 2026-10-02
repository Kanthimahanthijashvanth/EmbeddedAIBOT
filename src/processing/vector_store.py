from pathlib import Path

from langchain_chroma import Chroma


class WorkshopVectorStore:

    def __init__(
        self,
        embedding_function,
        persist_directory="vector_db",
        collection_name="workshop_rag"
    ):

        self.embedding_function = embedding_function

        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.collection_name = collection_name

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_function,
            persist_directory=str(
                self.persist_directory
            )
        )

    def add_documents(self, documents):

        if not documents:
            raise ValueError(
                "No documents provided."
            )

        ids = [
            document.metadata["chunk_id"]
            for document in documents
        ]

        self.vector_store.add_documents(
            documents=documents,
            ids=ids
        )

        return len(documents)

    def similarity_search(
        self,
        query,
        k=5
    ):

        return self.vector_store.similarity_search(
            query,
            k=k
        )

    def similarity_search_with_score(
        self,
        query,
        k=5
    ):

        return (
            self.vector_store
            .similarity_search_with_score(
                query,
                k=k
            )
        )

    def get_retriever(
        self,
        k=5
    ):

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k
            }
        )