from mcp.server import FastMCP


mcp = FastMCP("ProtonX demo server")

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers
    """
    return a * b

@mcp.tool()
def sum(a: int, b: int) -> int:
    """
    Sum two numbers
    """
    return a + b

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')