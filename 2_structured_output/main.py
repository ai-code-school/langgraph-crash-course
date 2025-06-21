from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class CountryDetails(BaseModel):
    """Detailed information about the country"""
    name: str = Field(description="Name of the country")
    national_language: str = Field(description="National Language of the country")
    other_languages: List[str] = Field(description="List of local languages spoken with in the country")
    capital: str = Field(description="Capital of the country")
    founder: str = Field(description="Who is the founder of the country, name of the person")
    borders: List[str] = Field(description="List the name of the countries it border with")

llm = ChatOllama(
    model="llama3.2:1b",
    base_url="http://localhost:11434",  # Default Ollama URL
    temperature=0.7  # Balanced creativity/consistency
)


def call_llm(user_input):
    message = [
            {"role": "system", "content" : "Your a smart agent and you tell interesting facts of the country asked by the user"},
            {"role": "user", "content" : user_input}
    ]
    return llm.invoke(message)

def call_llm_for_structured_output(user_input):
    message = [
        {"role": "system",
         "content": "Your a smart agent and you tell interesting facts of the country asked by the user"},
        {"role": "user", "content": user_input}
    ]
    structured_llm = llm.with_structured_output(CountryDetails)
    return structured_llm.invoke(message)

print(call_llm_for_structured_output("Tell me about England"))