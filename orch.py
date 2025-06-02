from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from websearch import web_search_agent
from yfinanceagent import yfinance_agent
from masterwebsearch import wavily
from fundamental import fundamentals_agent
from agno.models.google import Gemini
from sup2 import agentsup
from masterfinance import agent

valura_team = Team(
    name="Valura V-Suite",
    description=(
        "A squad of finance specialists. Each member first states "
        "if they can fully answer the query, then the coordinator "
        "selects the best ✓-agent, relays its answer verbatim, "
        "and adds a one-sentence wrap-up if needed."
    ),
    members=[yfinance_agent, agentsup, wavily],
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        # ── Coordination protocol ──────────────────────────
        "Step 1 – Broadcast the user query to **all members**.",
        "Step 2 – Each member must start its draft with either "
        "`CAN_HANDLE: YES – <reason>` or `CAN_HANDLE: NO – <reason>`.",
        "Step 3 – Pick the first `YES` with the *clearest* reason.",
        "Step 4 – Return that agent's answer **exactly as written**.",
        "Step 5 – If no agent says YES, reply:\n"
        "  'Sorry, none of my specialists can answer that.'",
        # ── Tone & misc. ───────────────────────────────────
        "Never expose internal IDs or tool names.",
        "Add a one-line executive summary if the specialist "
        "response is dense or highly technical.",
    ],
    mode="coordinate",
    show_members_responses=True,     # show agent coordination
    show_tool_calls=True,
    markdown=True,
)

# valura_team.print_response(
#     """
#     Recommend a low-risk bond with capital protection.
#     """,
#     markdown=True,
#     show_tool_calls=True,
# )