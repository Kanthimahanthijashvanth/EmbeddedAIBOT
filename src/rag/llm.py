from langchain_ollama import ChatOllama


class WorkshopLLM:

    def __init__(
        self,
        model_name="llama3.2:latest",
        temperature=0.3,
        num_ctx=2048
    ):

        self.model_name = model_name

        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            num_ctx=num_ctx
        )

    def invoke(self, prompt):

        return self.llm.invoke(prompt)