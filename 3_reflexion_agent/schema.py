from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="~250 word detailed answer to the question.")
    description: str = Field(description="1-3 search queries for researching improvements to address the critique of your current answer.")
    reflection: Reflection = Field(description="Your reflection on the initial answer. it includes 'missing' and 'superfluous'")
    search_queries: List[str] = Field(description="list 1 - 3 search queries separately")


def print_answer(result):
    print(f"Answer: {result.answer}")
    print(f"\nDescription: {result.description}")
    print("-" * 30)
    print("### Reflection ###")
    print(f"\nMissing: {result.reflection.missing}")
    print(f"\nSuperfluous: {result.reflection.superfluous}")


def invoke_with_retry(chain, input_data, max_retries=3):
    """Retry the chain invocation until we get tool calls"""
    result = []
    for attempt in range(max_retries):
        result = chain.invoke(input_data)

        # Check if we got tool calls
        if hasattr(result, 'tool_calls') and result.tool_calls:
            print(f"✅ Success on attempt {attempt + 1}")
            return result

        # Check if we got content but no tool calls
        output_tokens = result.usage_metadata.get('output_tokens', 0) if hasattr(result, 'usage_metadata') else 0
        if output_tokens > 10:  # Model generated content but didn't use tools
            print(f"⚠️  Attempt {attempt + 1}: Model generated {output_tokens} tokens but no tool calls")
        else:
            print(f"❌ Attempt {attempt + 1}: No significant response")

    print(f"❌ Failed after {max_retries} attempts")
    return result  # Return last attempt
