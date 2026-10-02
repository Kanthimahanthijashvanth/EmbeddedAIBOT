class ResourceFormatter:

    def format_document(self, document):

        metadata = document.metadata

        file_name = metadata.get(
            "file_name",
            "Unknown"
        )

        slide_number = metadata.get(
            "slide_number",
            metadata.get("page_number", "Unknown")
        )

        content_type = metadata.get(
            "content_type",
            "text"
        )

        chunk_id = metadata.get(
            "chunk_id",
            "Unknown"
        )

        content = document.page_content.strip()

        return (
            "[SOURCE]\n"
            f"File: {file_name}\n"
            f"Slide: {slide_number}\n"
            f"Type: {content_type}\n"
            f"Chunk: {chunk_id}\n"
            f"Content:\n{content}\n"
            "[/SOURCE]"
        )

    def format_documents(self, documents):

        formatted = []

        seen = set()

        for document in documents:

            content = document.page_content.strip()

            if not content:
                continue

            normalized = " ".join(
                content.split()
            ).lower()

            if normalized in seen:
                continue

            seen.add(normalized)

            formatted.append(
                self.format_document(document)
            )

        return "\n\n".join(formatted)