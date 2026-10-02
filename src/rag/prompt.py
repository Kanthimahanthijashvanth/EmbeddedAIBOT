from langchain_core.prompts import ChatPromptTemplate


class WorkshopPrompt:

    def __init__(self):

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a workshop assistant.

Answer the user's question using ONLY the provided workshop context.

Rules:
1. Do not invent information.
2. If the context does not contain the answer, say:
   "I could not find this information in the workshop material."
3. Give a clear and concise answer.
4. When using information from a source, mention its slide number.
5. Keep code exactly as provided when discussing code.
6. Distinguish between normal text, code, and tables when relevant.

Workshop context:
{context}
"""
            ),
            (
                "human",
                "{question}"
            )
        ])

    def format(
        self,
        context,
        question
    ):

        return self.prompt.invoke({
            "context": context,
            "question": question
        })