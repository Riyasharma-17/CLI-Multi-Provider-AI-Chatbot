from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import PydanticOutputParser

from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os


load_dotenv(override=True)

class MovieReview(BaseModel):

    title: str = Field(description="Movie title")

    rating: int = Field(description="Rating out of 10")

    summary: str = Field(description="Short review")


parser = PydanticOutputParser(
    pydantic_object=MovieReview
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "system",
                "You must return ONLY valid JSON.\n"
                "Do not include explanations, headings, markdown, or extra text.\n"
                "{format_instructions}"
)
        ),
        (
            "human",
            "{movie}"
        )
    ]
).partial(#Injects those format instructions into the prompt.
    format_instructions=parser.get_format_instructions()
)


chain = prompt | llm | parser


result = chain.invoke(
    {
        "movie": "Review Interstellar"
    }
)

print(result)

print(type(result))

print(result.title)

print(result.rating)

print(result.summary)