from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from masterfinance import agent
from websearch import web_search_agent
from yfinanceagent import yfinance_agent
from masterwebsearch import wavily
from fundamental import fundamentals_agent
from agno.models.google import Gemini
from sup2 import agentsup
from agno.models.openai import OpenAIResponses
from masterfinance import agent
from user_input import agentwebopen

valura_team = Team(
    name="Valura V-Suite",
    description=(
        "A squad of finance specialists. Each member first states "
        "if they can fully answer the query, then the coordinator "
        "selects the best ✓-agent, relays its answer verbatim, "
        "and adds a one-sentence wrap-up if needed."
    ),
    members=[yfinance_agent, agent, agentwebopen],
    model=OpenAIResponses(id="gpt-4o"),
    
    instructions=[
        # ── Core Response Protocol ──────────────────────────
        "Step 1 – Process user query and identify key requirements.",
        "Step 2 – Agents respond with `CAN_HANDLE: YES/NO` followed by a *single-line* reason.",
        "Step 3 – Select agent with most relevant capability match.",
        "Step 4 – Selected agent provides concise, focused response.",
        "Step 5 – If no capable agent, respond: 'No specialist available for this query.'",
        
        # ── Response Guidelines ────────────────────────────
        "Always include source attribution in [brackets]",
        "For news queries: Include latest timestamp and direct URL",
        "Keep responses under 3 paragraphs when possible",
        "Prioritize recent data (last 24-48 hours) for market/news queries",
        
        # ── Output Format ─────────────────────────────────
        "Structure complex responses with bullet points",
        "Add brief TL;DR for technical responses",
        "Use numerical data when available",
        
        # ── System Rules ───────────────────────────────────
        "Maintain professional tone",
        "Never expose system internals",
        "Focus on actionable insights",
    ],
    mode="coordinate",
        # show agent coordination
    
    markdown=True,
)
 

# valura_team.print_response(
#     """
#     Recommend a low-risk bond with capital protection.
#     """,
#     markdown=True,
#     show_tool_calls=True,
# )