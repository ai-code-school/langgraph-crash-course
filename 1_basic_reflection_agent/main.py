"""
Project: Viral YouTube Shorts Generator
Description: Generates and critiques YouTube Shorts content using LLMs via Ollama agents.
Author: Muhammad Mazhar Hassan
Date: 2025-06-20
Version: 1.0
License: MIT
"""
from langchain_core.messages import HumanMessage, AIMessage
from graph import app

def get_actor(obj):
    actor = "Unknown"
    if isinstance(obj, HumanMessage):
        actor = "Human"
    elif isinstance(obj, AIMessage):
        actor = "AI"
    return actor

def print_result(result):
    for x in result:
        print(f"""
{get_actor(x)}:
{x.content}
        """)
    print("*" * 20)

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

result = app.invoke("Intermittent fasting for beginners")
print_result(result)
