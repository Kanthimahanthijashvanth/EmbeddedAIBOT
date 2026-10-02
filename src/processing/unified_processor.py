from langchain_core.documents import Document

from src.ingestion.ingestion_pipeline import WorkshopIngestionPipeline
from src.processing.chunker import WorkshopChunker


class UnifiedProcessor:

    def __init__(
        self,
        data_dir="Data",
        chunk_size=800,
        chunk_overlap=100
    ):

        self.pipeline = WorkshopIngestionPipeline(
            data_dir=data_dir
        )

        self.chunker = WorkshopChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def process(self):

        results = self.pipeline.process_all()

        documents = []

        for result in results:

            # -----------------------------
            # PDF
            # -----------------------------

            if "slides" not in result:

                pdf_documents = self._process_pdf(
                    result["documents"]
                )

                documents.extend(pdf_documents)

            # -----------------------------
            # PPTX
            # -----------------------------

            else:

                structured_slides = result["slides"]

                ppt_documents = self.chunker.chunk(
                    structured_slides
                )

                documents.extend(
                    ppt_documents
                )

        return documents

    def _process_pdf(self, loaded_documents):

        documents = []

        for document in loaded_documents:

            text = document.page_content.strip()

            if not text:
                continue

            metadata = document.metadata.copy()

            metadata["content_type"] = "text"

            page_number = metadata.get(
                "page_number",
                "unknown"
            )

            workshop_id = metadata.get(
                "workshop_id",
                "unknown"
            )

            file_name = metadata.get(
                "file_name",
                "unknown"
            )

            # Semantic splitting of PDF page
            chunks = self.chunker.splitter.split_text(
                text
            )

            for chunk_number, chunk in enumerate(
                chunks,
                start=1
            ):

                chunk_id = (
                    f"{workshop_id}_"
                    f"page_{page_number}_"
                    f"chunk_{chunk_number}"
                )

                chunk_metadata = metadata.copy()

                chunk_metadata["chunk_id"] = chunk_id

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata=chunk_metadata
                    )
                )

        return documents