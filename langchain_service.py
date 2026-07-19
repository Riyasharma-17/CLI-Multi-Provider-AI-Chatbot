from dotenv import load_dotenv
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
# from langchain_openrouter import ChatOpenRouter

load_dotenv()


def get_llm(provider: str):

    if provider == "groq":
        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    # elif provider == "openrouter":
    #     return ChatOpenRouter(
    #         model="openrouter/auto"
    #     )

    raise ValueError("Unsupported provider")


def get_ai_response(
    question: str,
    provider: str
) -> str:

    llm = get_llm(provider)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant."),
            ("human", "{question}")
        ]
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain.invoke(
        {
            "question": question
        }
    )