class ResponseBuilder:

    def build(
        self,
        answer,
        documents
    ):

        citations = []

        seen = set()

        for document in documents:

            metadata = document.metadata

            file_name = metadata.get(
                "file_name",
                "Unknown"
            )

            slide_number = metadata.get(
                "slide_number",
                metadata.get("page_number", "Unknown")
            )

            citation = {
                "file_name": file_name,
                "slide_number": slide_number,
                "content_type": metadata.get(
                    "content_type",
                    "text"
                ),
                "chunk_id": metadata.get(
                    "chunk_id",
                    "Unknown"
                )
            }

            key = (
                file_name,
                slide_number
            )

            if key not in seen:
                seen.add(key)
                citations.append(citation)

        return {
            "answer": answer,
            "citations": citations
        }