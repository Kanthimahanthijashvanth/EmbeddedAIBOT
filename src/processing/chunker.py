from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class WorkshopChunker:

    def __init__(
        self,
        chunk_size=800,
        chunk_overlap=100
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk(self, structured_slides):

        documents = []

        for slide in structured_slides:

            slide_number = slide["slide_number"]

            source = slide["source"]
            file_name = slide["file_name"]
            workshop_id = slide["workshop_id"]

            content = slide["content"]

            chunk_counter = 0

            # --------------------------------
            # NORMAL TEXT
            # --------------------------------

            text_parts = []

            for item in content["text"]:

                text = item["content"].strip()

                if text:
                    text_parts.append(text)

            combined_text = "\n".join(text_parts)

            if combined_text:

                chunks = self.splitter.split_text(
                    combined_text
                )

                for chunk in chunks:

                    chunk_counter += 1

                    documents.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "workshop_id": workshop_id,
                                "file_name": file_name,
                                "source": source,
                                "slide_number": slide_number,
                                "content_type": "text",
                                "chunk_id": (
                                    f"{workshop_id}_"
                                    f"slide_{slide_number}_"
                                    f"chunk_{chunk_counter}"
                                )
                            }
                        )
                    )

            # --------------------------------
            # CODE
            # --------------------------------

            for item in content["code"]:

                code = item["content"].strip()

                if not code:
                    continue

                chunk_counter += 1

                documents.append(
                    Document(
                        page_content=code,
                        metadata={
                            "workshop_id": workshop_id,
                            "file_name": file_name,
                            "source": source,
                            "slide_number": slide_number,
                            "content_type": "code",
                            "chunk_id": (
                                f"{workshop_id}_"
                                f"slide_{slide_number}_"
                                f"chunk_{chunk_counter}"
                            )
                        }
                    )
                )

            # --------------------------------
            # TABLES
            # --------------------------------

            for table_number, table in enumerate(
                content["tables"],
                start=1
            ):

                rows = table.get("rows", [])

                if not rows:
                    continue

                table_text = self._table_to_text(
                    rows
                )

                if not table_text:
                    continue

                chunk_counter += 1

                documents.append(
                    Document(
                        page_content=table_text,
                        metadata={
                            "workshop_id": workshop_id,
                            "file_name": file_name,
                            "source": source,
                            "slide_number": slide_number,
                            "content_type": "table",
                            "table_number": table_number,
                            "chunk_id": (
                                f"{workshop_id}_"
                                f"slide_{slide_number}_"
                                f"chunk_{chunk_counter}"
                            )
                        }
                    )
                )

        return documents

    def _table_to_text(self, rows):

        formatted_rows = []

        for row in rows:

            row_text = " | ".join(
                cell.strip()
                for cell in row
            )

            if row_text.strip():
                formatted_rows.append(row_text)

        return "\n".join(formatted_rows)