
## MCP Server Experiments

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended for faster dependency management)

## Installation

1. Install `uv` package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   For more details, visit: https://docs.astral.sh/uv/#installation

2. Init a project
```
uv init <project-name>
```

3. Install MCP with CLI support:
   ```bash
   uv add "mcp[cli]"
   ```

## Running the Server

To start the MCP server:
```bash
mcp dev server.py
```

To test some concepts, go to the `core-concepts` directory and run the server:

```bash
cd core-concepts/resource-concept
mcp dev server.py
```


