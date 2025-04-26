from typing import TypedDict, Literal
from IPython.display import display
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    query: str
    
    
def node_1(state: AgentState):
    print("---Node 1---")
    return {
        "graph_state": state["graph_state"]
    }

def node_2(state: AgentState):
    print("---Node 2---")
    return {
        "graph_state": state["graph_state"] + ". I live coding."
    }

def node_3(state: AgentState):
    print("---Node 3---")
    return {
        "graph_state": state["graph_state"] + "I live gymming."
    }

def decision_node(state: AgentState) -> Literal["node_2", "node_3"]:
    user_input = state["graph_state"]
    
    if "coder" in user_input.lower():
        return "node_2"
    
    return "node_3"


builder = StateGraph(AgentState)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_conditional_edges(
    "node_1",
    decision_node,
)

builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

compiled_graph = builder.compile()


# Get the PNG data
png_data = compiled_graph.get_graph().draw_mermaid_png()

# Save the PNG data to a file
with open('mermaid_graph.png', 'wb') as f:
    f.write(png_data)

print("Graph saved as 'mermaid_graph.png'")





