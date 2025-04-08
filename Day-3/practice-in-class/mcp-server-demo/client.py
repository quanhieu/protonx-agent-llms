import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        # self.openai = OpenAI()
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

    async def process_query(self, query: str) -> str:
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()

        available_tools = [{ 
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # print(f"Available tools: {available_tools}")
        response = self.anthropic.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
            system="To answer the user's question, you must use the provided tools",
            tool_choice= {
                "type": "any"
            }
        )

        print(f"Response: {response}")

        for content in response.content:
            if content.type == 'text':
                return content.text
            elif content.type == 'tool_use':
                # print(f"Tool use: {content}")
                tool_name = content.name
                tool_args = content.input

                # print(f"Calling tool {tool_name} with args {tool_args}")
                result = await self.session.call_tool(tool_name, tool_args)
                # print(f"Tool {tool_name} returned: {result}")

                return result.content[0].text

        return "No response from tools"

        
    

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # # List available tools
        # response = await self.session.list_tools()
        # tools = response.tools
        # print("\nConnected to server with tools:", [tool.name for tool in tools])

        # result = await self.session.call_tool("sum", {
        #         "a": 1,
        #         "b": 2
        #     })


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                answer = await client.process_query(query)
                print(answer)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    finally:
        await client.cleanup()
        print("Client disconnected")

if __name__ == "__main__":
    import sys
    asyncio.run(main())