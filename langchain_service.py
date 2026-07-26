from dotenv import load_dotenv
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from openai import RateLimitError

load_dotenv()

# Change ONLY this line whenever you want to test another OpenRouter model
OPENROUTER_MODEL = "google/gemma-4-26b-a4b-it:free"


def get_llm(provider: str):

    if provider == "groq":
        print("========== GROQ ==========")
        print("Using model: llama-3.1-8b-instant")

        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    elif provider == "openrouter":
        print("========== OPENROUTER ==========")
        print(f"Using model: {OPENROUTER_MODEL}")

        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

    else:
        raise ValueError("Unsupported provider")


def get_ai_response(
    question: str,
    provider: str
) -> str:

    llm = get_llm(provider)

    print(f"Provider selected: {provider}")
    print(llm)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant."),
            ("human", "{question}")
        ]
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    try:
        return chain.invoke(
            {
                "question": question
            }
        )

    except RateLimitError:
        return (
            "⚠️ The selected OpenRouter free model is currently busy or rate-limited. "
            "Please try again after a few minutes or choose another provider/model."
        )

    except Exception as e:
        msg = str(e)

        if "ResourceExhausted" in msg or "Worker local total request limit reached" in msg:
            return (
                "⚠️ This OpenRouter free model is currently overloaded. "
                "Please try again in a few minutes or switch to another model."
            )

        print("ERROR:", e)
        return f"Error: {msg}"