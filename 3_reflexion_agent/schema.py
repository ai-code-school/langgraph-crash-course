from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="~250 word detailed answer to the question.")
    description: str = Field(description="1-3 search queries for researching improvements to address the critique of your current answer.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")


def print_answer(result):
    print(f"Answer: {result.answer}")
    print(f"\nDescription: {result.description}")
    print("-" * 30)
    print("### Reflection ###")
    print(f"\nMissing: {result.reflection.missing}")
    print(f"\nSuperfluous: {result.reflection.superfluous}")