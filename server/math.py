from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("math")


@mcp.tool()
async def compare(num1: float, num2: float) -> str:
    """Compare num1 and num2.

    Args:
        num1: num1
        num2: num2
    """
    if num1 > num2:
        return f"{num1} is larger than {num2}"
    elif num1 < num2:
        return f"{num1} is smaller than {num2}"
    else:
        return f"{num1} is equal to {num2}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
