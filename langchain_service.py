# This file will contain all LangChain-related code.

from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)


# Returns the required LLM based on the provider name.
def get_llm(provider: str):

    if provider == "groq":
        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    raise ValueError("Unsupported provider")


# Change ONLY this line to switch models.
#llm = get_llm("groq")
llm = get_llm("gemini")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        ("human", "{question}")
    ]
)

# Converts AIMessage -> plain Python string
parser = StrOutputParser()

# LCEL Chain
chain = prompt | llm | parser


# Temporary testing
if __name__ == "__main__":

    result = chain.invoke(
        {
            "question": "Explain LangChain in 2 lines."
        }
    )

    print(result)