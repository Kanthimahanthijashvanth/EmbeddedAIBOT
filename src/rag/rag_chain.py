class WorkshopRAGChain:

    def __init__(
        self,
        retriever,
        context_builder,
        prompt_builder,
        response_builder,
        llm=None,
        k=5
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.response_builder = response_builder
        self.llm = llm
        self.k = k

    def prepare(self, question):

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        documents = self.retriever.retrieve(
            question
        )

        context = self.context_builder.build(
            documents
        )

        prompt = self.prompt_builder.format(
            context=context,
            question=question
        )

        return {
            "question": question,
            "documents": documents,
            "context": context,
            "prompt": prompt
        }

    def invoke(self, question):

        prepared = self.prepare(question)

        if self.llm is None:
            raise ValueError(
                "LLM is not configured. "
                "Pass an LLM when creating WorkshopRAGChain."
            )

        response = self.llm.invoke(
            prepared["prompt"]
        )

        # LangChain chat models normally return
        # an AIMessage with a .content attribute.
        if hasattr(response, "content"):
            answer = response.content
        else:
            answer = str(response)

        result = self.response_builder.build(
            answer=answer,
            documents=prepared["documents"]
        )

        result["question"] = question

        return result