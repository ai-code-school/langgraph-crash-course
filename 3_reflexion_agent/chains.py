import datetime

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser

from schema import AnswerQuestion, print_answer
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

pydantic_parser = PydanticToolsParser(tools = [AnswerQuestion])


llm = ChatOllama(
    model="llama3.2:1b", #Model of your choice
    base_url="http://localhost:11434",  # Default Ollama URL
    temperature=0.7  # Balanced creativity/consistency
)

actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system",
    """You are expert AI researcher.
    Current time: {time}
    1. {first_instruction}
    2. Reflect and critique your answer.Be severe to maximize improvement.
    3.After the reflection, ** list 1 - 3 search queries separately ** for researching improvements.Do not include them inside the reflection.
""",),
    MessagesPlaceholder (variable_name="messages"),
    ("system", "Answer the user's question above using the required format.")
    ,
    ]).partial(
        time= lambda: datetime.datetime.now().isoformat(),
    )

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = "Provide a detailed ~250 words answer"
)


# Replace PydanticToolsParser with structured output
answer_llm = llm.with_structured_output(AnswerQuestion)

#first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') | pydantic_parser
first_responder_chain = first_responder_prompt_template | answer_llm


if __name__ == "__main__":
    result = first_responder_chain.invoke({
        "messages":[HumanMessage(content="Write a lifestyle blog post about how people over 40 can stay healthy and active, including strategies for maintaining a healthy weight.")]
    })
    print_answer(result)
