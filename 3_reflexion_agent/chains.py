import datetime

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser

from llm_helper import invoke_with_tools_retry
from schema import AnswerQuestion, print_answer
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from message_parser import extract_answer_tools, parse_ollama_response

pydantic_parser = PydanticToolsParser(tools = [AnswerQuestion])


llm = ChatOllama(
    model="llama3.1:8b", #Model of your choice
    base_url="http://localhost:11434",  # Default Ollama URL
    temperature=0.7  # Balanced creativity/consistency
)


actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI researcher.
    Current time: {time}
    1. {first_instruction}
    2. Reflect and critique your answer in this format with 'missing' and 'superfluous'
    3. list 3 search queries for researching improvements. 
    
    You must use the AnswerQuestion tool to provide your response."""
    ),
    MessagesPlaceholder(variable_name="messages"),
]).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = "Provide a detailed ~250 words answer"
)

#first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') | pydantic_parser
answer_llm_x = llm.bind_tools(tools=[AnswerQuestion], tool_choice="any")
first_responder_chain = first_responder_prompt_template | answer_llm_x

if __name__ == "__main__":
    print("Invoking change with user question")
    messages = [
        HumanMessage(content="Create a blog post about building confidence through public speaking")
    ]

    chain_result = invoke_with_tools_retry(first_responder_chain, {"messages": messages}, max_retries=3)
    print(f"Chain result\n{chain_result}")
    print(f"Chain tool calls: {getattr(chain_result, 'tool_calls', 'No tool_calls')}")
    print()
    print("Parsed contents:")
    print(parse_ollama_response(chain_result))

