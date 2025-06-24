from typing import TypedDict
from langgraph.graph import END, StateGraph

class SimpleCounter(TypedDict):
    counter: int


def increment(state:SimpleCounter) -> SimpleCounter:
    return {
        "counter" : state["counter"] + 1
    }

def should_continue(state):
    if state["counter"] < 5:
        return "continue"
    else:
        return "stop"

graph = StateGraph(SimpleCounter)
graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment", should_continue, {
    "continue" : "increment",
    "stop": END
})

app = graph.compile()
result = app.invoke({"counter": 0})
print(result)