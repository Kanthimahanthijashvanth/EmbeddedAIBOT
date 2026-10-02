from src.rag.resource_formatter import ResourceFormatter


class ContextBuilder:

    def __init__(self, max_documents=5):

        self.max_documents = max_documents

        self.formatter = ResourceFormatter()

    def build(self, documents):

        if not documents:
            return ""

        documents = documents[:self.max_documents]

        return self.formatter.format_documents(
            documents
        )