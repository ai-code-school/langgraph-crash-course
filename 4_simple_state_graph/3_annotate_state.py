import operator
from typing import TypedDict, List, Annotated
from langgraph.graph import END, StateGraph

class SimpleCounter(TypedDict):
    counter: int
    sum: Annotated[int, operator.add]
    history: Annotated[List[int], operator.concat]

def increment(state:SimpleCounter) -> SimpleCounter:
    counter = state["counter"] + 1
    return {
        "counter" : counter,
        "sum": counter,
        "history": [counter]
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
result = app.invoke({"counter": 0, "sum":0, "history":[]})
print(result)