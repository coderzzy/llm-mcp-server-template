import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load environment variables from .env

def test_openai():
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1",
        input="Write a one-sentence bedtime story about a unicorn."
    )
    print(response.output_text)

def test_openai_agent():
    # 测试代码
    agent = Agent(name="TestAgent", instructions="Return 'Setup successful'")
    result = Runner.run_sync(agent, "Run test")
    print(result.final_output)  # Expected output: "Setup successful"


async def main():
    # agent not use mcp
    agent_without_mcp = Agent(
        name="Assistant",
        model="gpt-4o-mini",
        instructions="Solve Math Problems.",
    )
    result_without_mcp = Runner.run_streamed(
        starting_agent=agent_without_mcp, input="which one is larger, 9.11 or 9.3?"
    )
    print("the result of agent-without-mcp is: ")
    async for event in result_without_mcp.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data.delta, end="", flush=True)

    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as server:
        # List tools provided by the MCP server
        tools = await server.list_tools()

        samples_dir = "～/Desktop"
        # agent that uses the MCP server
        agent_with_mcp = Agent(
            name="Assistant",
            model="gpt-4o-mini",
            instructions="Use the filesystem tools to help the user with their tasks.",
            mcp_servers=[server],
        )
        result_with_mcp = await Runner.run(
            starting_agent=agent_with_mcp, input="List the files in the directory."
        )
        print("the result of agent-with-mcp is: ", result_with_mcp.final_output)


if __name__ == "__main__":
    # asyncio.run(main())
    test_openai()
