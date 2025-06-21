from langchain_ollama import ChatOllama


# Define LLM that we are going to use
#---------------------------------------
# We can down load and Ollama(A tool to interact with model) locally
# Download a model `ollama pull llama3.2:1b`
# List locally available models `ollama list`
#---------------------------------------
llm = ChatOllama(
    model="llama3.2:1b", #Model of your choice
    base_url="http://localhost:11434",  # Default Ollama URL
    temperature=0.7  # Balanced creativity/consistency
)

# Set up a helper function that helps in querying the LLM
# with pre-defined system prompt
def query_llm(user_input):
    message = [
            {"role": "system", "content" : "Your a smart agent and you tell interesting facts of the country asked by the user"},
            {"role": "user", "content" : user_input}
    ]
    return llm.invoke(message)

# Make a call
print(query_llm("Tell me about England"))