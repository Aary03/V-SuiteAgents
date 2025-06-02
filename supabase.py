import os
import asyncio
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools

SUPABASE_ACCESS_TOKEN = "sbp_632e6f006b67f4a82b612ae9cca0d15c0fa8c5ac"

async def run_agent(question: str):
    # Set the token in the environment for MCPTools
    os.environ["SUPABASE_ACCESS_TOKEN"] = SUPABASE_ACCESS_TOKEN

    npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
    async with MCPTools(
        f"{npx_cmd} -y @supabase/mcp-server-supabase@latest --access-token={SUPABASE_ACCESS_TOKEN}"
    ) as mcp:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            instructions=(
                "You are a Supabase expert. "
                "Given a user question, use the available Supabase MCP tools to fetch the required information from Supabase. "
                "Return only the answer to the user's question, formatted in markdown if appropriate."
            ),
            tools=[mcp, ReasoningTools(add_instructions=True)],
            markdown=True,
        )
        await agent.aprint_response(
            message=question,
            stream=True,
            stream_intermediate_steps=True,
            show_full_reasoning=True,
        )

if __name__ == "__main__":
    # Example: Replace this with any question you want to ask about your Supabase project
    question = "List all tables in my Supabase project and show their row counts."
    asyncio.run(run_agent(question))