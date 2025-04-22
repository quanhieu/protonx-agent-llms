from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Agent-01-class-day-4")

@mcp.tool(
    name="count_students",
    description=
    f"Count the number of students in a class with gender\n" + 
    f"class_name: The name of the class to count students in\n" + 
    f"return: The number of students in the class\n" + 
    f"Input: Lớp agent-01 có bao nhiêu học sinh nam? -> count_students(name='agent-01', gender='male')" + 
    f"Input: Lớp agent-01 có bao nhiêu học sinh nữ? -> count_students(name='agent-01', gender='female')"
)
def count_students(class_name: str, gender: str) -> int:
    if class_name == "agent-01":
        if gender == "male":
            return 137
        else:
            return 20
    else:
        return 0

@mcp.resource("file:///logs/app.log", name="Application Logs", mime_type="text/plain")
def get_logs() -> str:
    """Sample application logs"""
    return "2025-04-15 12:00:00 INFO Starting application\n2025-04-15 12:00:05 INFO Connected to database\n2025-04-15 12:01:10 WARN High memory usage detected"


# Add this at the end of your file
if __name__ == "__main__":
    # Start the MCP server
    mcp.run()