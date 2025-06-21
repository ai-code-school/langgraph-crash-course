"""
Project: Viral YouTube Shorts Generator
Description: Generates and critiques YouTube Shorts content using LLMs via Ollama agents.
Author: Muhammad Mazhar Hassan
Date: 2025-06-20
Version: 1.0
License: MIT
"""

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from chains import critique_chain, content_generation_chain

CONTENT_NODE = "content"
CRITIQUE_NODE = "critique"

# Define Agents
def content_node(state):
    return content_generation_chain.invoke({
        "history": state
    })

def critique_node(state):
    last_content = next((msg for msg in reversed(state) if msg.type == "ai"), None)

    if not last_content:
        return [HumanMessage(content="No content found to critique.")]

    response = critique_chain.invoke({
        "topic": last_content.content,
        "history": state
    })

    return [HumanMessage(content=response.content.strip() or "All looks good, lets conclude this")]


def keep_refining(state):
    if len(state) > 4:
        return END
    return CRITIQUE_NODE

graph = MessageGraph()

#define nodes
graph.add_node(CONTENT_NODE, content_node)
graph.add_node(CRITIQUE_NODE, critique_node)

#define edges
graph.set_entry_point(CONTENT_NODE)
graph.add_conditional_edges(CONTENT_NODE, keep_refining, {
        CRITIQUE_NODE: CRITIQUE_NODE,
        END: END,
    })
graph.add_edge(CRITIQUE_NODE, CONTENT_NODE)

#compile graph
app = graph.compile()

