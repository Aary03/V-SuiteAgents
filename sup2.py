import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.models.openai import OpenAIChat
from memoryset import memory,storage
from dotenv import load_dotenv

load_dotenv()

if "SUPABASE_ACCESS_TOKEN" not in os.environ:
    raise ValueError("SUPABASE_ACCESS_TOKEN not set.")

if "SUPABASE_PROJECT_REF" not in os.environ:
    raise ValueError("SUPABASE_PROJECT_REF not set.")

# Launch the Supabase MCP server
command = (
    f"mcp-server-supabase "
    f"--access-token={os.environ['SUPABASE_ACCESS_TOKEN']} "
    f"--project-ref={os.environ['SUPABASE_PROJECT_REF']} "
    f"--read-only"
)

# Create the agent
mcp_tools = MCPTools(command)

agentsup = Agent(
    name="ProductExpert",
    role="A helpful assistant that understands and recommends financial products like bonds, funds, and structured products based on user needs.",
    model=OpenAIChat(id="gpt-4o"),
    memory=memory,
    storage=storage,
    enable_agentic_memory=True,
    enable_user_memories=True,
    tools=[mcp_tools],
    instructions=dedent("""
         CAN-HANDLE flag:
      Write `CAN_HANDLE: YES – <reason>` if the user is asking for
      product selection, filtering, or catalogue look-ups that can
      be satisfied with SQL on `ProductCatalogue`.
      Otherwise reply `CAN_HANDLE: NO – <reason>` and stop.

    Data access:
      • Use *read-only* SELECT … WHERE …
      • Never modify data.

    Answer structure:
      1. Brief intro (≤20 words).
      2. Table of key fields (Name, Type, Risk, Return, Maturity).
      3. One bullet of commentary per product.

        Compliance:
      • No advice; describe features and risks neutrally.
      • End with: '_Source: Valura ProductCatalogue. Not advice._'
        You are familiar with a table named `ProductCatalogue` in Supabase that contains financial products.

        Use SQL SELECT queries to find suitable products based on user preferences such as:
        - Risk level
        - Return percentage
        - Capital protection
        - Product type (Bond, Fund, Structured Product)
        - Maturity period

        Provide helpful summaries and suggestions, and format results as a table when appropriate.
        Avoid modifying any data or making assumptions not based on available information.
    """),
    show_tool_calls=True,
    markdown=True,
    add_state_in_messages=True,
)


# import asyncio

# # async def run_query():
# #     await agentsup.aprint_response("Recommend a low-risk bond with capital protection.")

# # asyncio.run(run_query())
