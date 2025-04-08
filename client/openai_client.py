import os
os.environ["OPENAI_API_KEY"] = ""

from agents import Agent, Runner

if __name__ == "__main__":
    agent = Agent(name="TestAgent", instructions="Return 'Setup successful'")
    result = Runner.run_sync(agent, "Run test")
    print(result.final_output)  