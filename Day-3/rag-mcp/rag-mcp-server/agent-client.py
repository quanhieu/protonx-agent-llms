import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from agents import Agent, Runner, gen_trace_id, trace, function_tool, handoff, RunContextWrapper
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings
from mcp import ClientSession
from mcp.client.sse import sse_client

async def list_prompts(session: ClientSession):
    response = await session.list_prompts()
    return response

async def get_prompt(session: ClientSession, prompt_name: str):
    response = await session.get_prompt(prompt_name)
    return response

async def run(mcp_server: MCPServer, promps: dict):

    # Currently agent of openai only support list tools 
    # so if we need to list prompts, we need to initialize the new session here

    product_agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )


    manager_agent = Agent(
        name="manager",
        instructions=promps["MANAGER_INSTRUCTION"],
        handoffs=[
            handoff(
                product_agent,
            )
        ]
        
    )


    # Run the `get_secret_word` tool
    message = "3210 4gb"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=manager_agent, input=message)
    print(result.final_output)

async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:
        trace_id = gen_trace_id()
        # Use a single async with block for the sse_client
        async with sse_client(url="http://localhost:8000/sse") as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                
                prompt_response = await session.get_prompt(name="manager_prompt")
                MANAGER_INSTRUCTION = prompt_response.messages[0].content.text
                
                with trace(workflow_name="SSE Example", trace_id=trace_id):
                    print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
                    await run(server, {
                        "MANAGER_INSTRUCTION": MANAGER_INSTRUCTION
                    })

if __name__ == "__main__":
    # Let's make sure the user has uv installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # We'll run the SSE server in a subprocess. Usually this would be a remote server, but for this
    # demo, we'll run it locally at http://localhost:8000/sse
    process: subprocess.Popen[Any] | None = None
    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        server_file = os.path.join(this_dir, "server.py")

        print("Starting SSE server at http://localhost:8000/sse ...")

        # Run `uv run server.py` to start the SSE server
        process = subprocess.Popen(["uv", "run", server_file])
        # Give it 3 seconds to start
        time.sleep(3)

        print("SSE server started. Running example...\n\n")
    except Exception as e:
        print(f"Error starting SSE server: {e}")
        exit(1)

    try:
        asyncio.run(main())
    finally:
        if process:
            process.terminate()