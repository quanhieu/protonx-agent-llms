from agents import Agent, Runner, function_tool, handoff, RunContextWrapper, trace
from agents.extensions import handoff_filters
from agents.handoffs import HandoffInputData
from rag import rag

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

product_agent = Agent(
    name="product",
    instructions="Search product information and answer the question",
    tools=[
        rag,
    ]
)

result = asyncio.run(Runner.run(product_agent, "nokia 3210"))
print(result)