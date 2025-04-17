import asyncio
import re

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load environment variables from .env


def test_openai():
    # 最原始的OpenAI调用
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
    )
    print(response.output_text)


def test_openai_agent():
    # 测试OpenAI Agent
    agent = Agent(name="TestAgent", instructions="Return 'Setup successful'")
    result = Runner.run_sync(agent, "Run test")
    print(result.final_output)  # Expected output: "Setup successful"


async def test_openai_agent_with_mcp():
    # 测试OpenAI Agent with MCP Server
    samples_dir = "～/Desktop"
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as server:
        # List tools provided by the MCP server
        tools = await server.list_tools()

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


async def main():
    # agent not use mcp
    agent_without_mcp = Agent(
        name="Assistant",
        model="gpt-4o-mini",
        instructions="Solve Math Problems.",
    )
    result_without_mcp = await Runner.run(
        starting_agent=agent_without_mcp, input="compare which one is larger, 9.11 or 9.3?"
    )
    print("the result of agent-without-mcp is: ", result_without_mcp.final_output)

    # agent use mcp
    async with MCPServerStdio(
        params={
            "command": "uv",
            "args": ["--directory", "../server", "run", "math.py"],
        }
    ) as server:
        # List tools provided by the MCP server
        tools = await server.list_tools()

        # agent that uses the MCP server
        agent_with_mcp = Agent(
            name="Assistant",
            model="gpt-4o-mini",
            instructions="Solve Math Problems.",
            mcp_servers=[server],
        )
        result_with_mcp = await Runner.run(
            starting_agent=agent_with_mcp, input="compare which one is larger, 9.11 or 9.3?"
        )
        print("the result of agent-with-mcp is: ", result_with_mcp.final_output)


if __name__ == "__main__":
    # test_openai()
    # test_openai_agent()
    # asyncio.run(test_openai_agent_with_mcp())
    asyncio.run(main())
