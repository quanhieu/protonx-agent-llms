from typing import TypedDict, List, Dict, Any, Optional, Literal
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from utils import print_welcome_banner
from dotenv import load_dotenv
load_dotenv()

# Import your existing RAG tools and prompts
from rag import rag, shop_information_rag
from prompt import MANAGER_INSTRUCTION, PRODUCT_INSTRUCTION, SHOP_INFORMATION_INSTRUCTION

# Initialize our LLM
model = ChatOpenAI(temperature=0)

# Define our State
class AgentState(TypedDict):
    # The query being processed
    query: str
    # The conversation history
    messages: List[Dict[str, Any]]
    # Agent routing
    routing_decision: Optional[str]
    # RAG results
    product_rag_results: Optional[str]
    shop_info_rag_results: Optional[str]
    # Final response
    response: Optional[str]

# Define our Nodes (processing functions)
def process_query(state: AgentState):
    """Initial processing of the query"""
    print(f"\n[System] Processing query: {state['query']}")
    return {}

def determine_agent(state: AgentState):
    """Manager agent determines which specialized agent should handle the query"""
    query = state["query"]
    messages = state["messages"]
    
    # Prepare prompt for the LLM
    prompt = f"""
    {MANAGER_INSTRUCTION}
    
    User query: {query}
    
    Based on this query, determine if it should be handled by:
    1. "product" - for product related queries
    2. "shop_information" - for store information, hours, location, etc.
    
    Respond with just one word: either "product" or "shop_information".
    """
    
    # Call the LLM
    messages_for_llm = [HumanMessage(content=prompt)]
    response = model.invoke(messages_for_llm)
    
    # Parse the response to get routing decision
    response_text = response.content.lower().strip()
    routing_decision = None
    
    if "product" in response_text:
        routing_decision = "product"
    elif "shop_information" in response_text:
        routing_decision = "shop_information"
    else:
        # Default to product if unclear
        routing_decision = "product"
    
    print(f"[System] Routing decision: {routing_decision}")
    
    # Return state updates
    return {
        "routing_decision": routing_decision
    }

def handle_product_query(state: AgentState):
    """Product agent handles product-related queries using RAG"""
    query = state["query"]
    messages = state["messages"]
    
    # Use your existing RAG function
    rag_results = rag(query)
    print(f"[System] Retrieved product information")
    
    # Prepare prompt for the LLM with RAG context
    prompt = f"""
    {PRODUCT_INSTRUCTION}
    
    User query: {query}
    
    RAG results: {rag_results}
    
    Based on the provided information, answer the user's product-related question.
    """
    
    # Call the LLM
    messages_for_llm = [HumanMessage(content=prompt)]
    response = model.invoke(messages_for_llm)
    
    # Return state updates
    return {
        "product_rag_results": rag_results,
        "response": response.content
    }

def handle_shop_information_query(state: AgentState):
    """Shop information agent handles store-related queries using RAG"""
    query = state["query"]
    messages = state["messages"]
    
    # Use your existing RAG function
    rag_results = shop_information_rag()
    print(f"[System] Retrieved shop information")
    
    # Prepare prompt for the LLM with RAG context
    prompt = f"""
    {SHOP_INFORMATION_INSTRUCTION}
    
    User query: {query}
    
    RAG results: {rag_results}
    
    Based on the provided information, answer the user's question about the shop.
    """
    
    # Call the LLM
    messages_for_llm = [HumanMessage(content=prompt)]
    response = model.invoke(messages_for_llm)
    
    # Return state updates
    return {
        "shop_info_rag_results": rag_results,
        "response": response.content
    }

def format_response(state: AgentState):
    """Format the final response to return to the user"""
    # In this simple case, we just return the response directly
    # You could add additional formatting here if needed
    print(f"[System] Preparing response")
    return {}

# Define routing logic
def route_query(state: AgentState) -> str:
    """Determine which agent should handle the query"""
    if state["routing_decision"] == "product":
        return "product"
    else:
        return "shop_information"

# Create the StateGraph
agent_graph = StateGraph(AgentState)

# Add nodes
agent_graph.add_node("process_query", process_query)
agent_graph.add_node("determine_agent", determine_agent)
agent_graph.add_node("handle_product_query", handle_product_query)
agent_graph.add_node("handle_shop_information_query", handle_shop_information_query)
agent_graph.add_node("format_response", format_response)

# Define the flow
agent_graph.add_edge(START, "process_query")
agent_graph.add_edge("process_query", "determine_agent")

# Add conditional branching from determine_agent
agent_graph.add_conditional_edges(
    "determine_agent",
    route_query,
    {
        "product": "handle_product_query",
        "shop_information": "handle_shop_information_query"
    }
)

# Add the final edges
agent_graph.add_edge("handle_product_query", "format_response")
agent_graph.add_edge("handle_shop_information_query", "format_response")
agent_graph.add_edge("format_response", END)

# Compile the graph
compiled_graph = agent_graph.compile()

def main():
    print_welcome_banner()
    
    # Set up conversation history
    conversation_history = []
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye! Have a great day!")
            break
        
        # Prepare the input state for the graph
        input_state = {
            "query": user_input,
            "messages": conversation_history + [{"role": "user", "content": user_input}],
            "routing_decision": None,
            "product_rag_results": None,
            "shop_info_rag_results": None,
            "response": None
        }
        
        # Invoke the graph with the input state
        result = compiled_graph.invoke(input_state)
        
        # Update conversation history
        conversation_history = input_state["messages"] + [{"role": "assistant", "content": result["response"]}]
        
        # Display the assistant's response
        print(f"\nAssistant: {result['response']}")

if __name__ == "__main__":
    main()