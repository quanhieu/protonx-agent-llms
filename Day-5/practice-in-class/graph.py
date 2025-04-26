from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    graph_state: str

def xac_dinh_dep_trai_hay_dep_gai(state):
    print('--state--', state)
    return {
        "graph_state": state["graph_state"]
    }
    
def dep_trai_thi_lam_gi(state):
    print('--dep_trai_thi_lam_gi state--', state)
    return {
        "graph_state": state["graph_state"]
    }
    

def dep_gai_thi_lam_gi(state):
    print('--dep_gai_thi_lam_gi state--', state)
    return {
        "graph_state": state["graph_state"]
    }


def decision_logic(state):  
    if state["graph_state"] == "dep trai":
        return "dep_trai"
    else:
        return "dep_gai"


builder = StateGraph(AgentState)

builder.add_node("xac_dinh_dep_trai_hay_dep_gai", xac_dinh_dep_trai_hay_dep_gai)
builder.add_node("dep_trai_thi_lam_gi", dep_trai_thi_lam_gi)
builder.add_node("dep_gai_thi_lam_gi", dep_gai_thi_lam_gi)

builder.add_edge(START, "xac_dinh_dep_trai_hay_dep_gai")

builder.add_conditional_edges(
    "xac_dinh_dep_trai_hay_dep_gai",
   decision_logic,
   {
       "dep_trai": "dep_trai_thi_lam_gi",
       "dep_gai": "dep_gai_thi_lam_gi"
   }
)


builder.add_edge("dep_trai_thi_lam_gi", END)
builder.add_edge("dep_gai_thi_lam_gi", END)


compiled_graph = builder.compile()

inputs = {
    "graph_state": "dep gai"
}
# for state in compiled_graph.stream(inputs, stream_mode="values"):
#    print(state)

compiled_graph.invoke(inputs)





