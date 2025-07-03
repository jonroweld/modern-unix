from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather", stateless_http=True)


@mcp.tool()  # Using this mcp instance
async def get_forecast(city: str) -> str:
    """Get weather forecast for a city.

    Args:
        city(str): The name of the city
    """
    return f"The weather in {city} will be warm and sunny"

mcp_stateless = mcp.streamable_http_app()