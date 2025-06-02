# ── Valura.ai • Wavily Mega-Search Agent ──────────────────────────────────────
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.reasoning import ReasoningTools
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from memoryset import memory,storage
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

wavily = Agent(
    name="Wavily",
    role=(
        "A cost-aware web-research analyst. It finds the *minimum* set of "
        "high-quality sources needed to answer an investor query, then delivers "
        "a concise, referenced brief."
    ),
    model=OpenAIChat(id="gpt-4o"),               # ⅔ cheaper than gpt-4o for research tasks
    memory=memory,
    storage=storage,
    enable_agentic_memory=True,
    enable_user_memories=True,
    tools=[
        TavilyTools(search=True,include_answer = True,cache_results=True),      # start cheap; escalate only if needed),
        ReasoningTools(add_instructions=True),
    ],
    add_history_to_messages=True,       # allows caching & avoids repeat queries
    instructions=[
        # ── Cost discipline ────────────────────────────────────────────────
        "Phase 1: Run Tavily basic search with max_results=3.",
        "Phase 2: Parse relevance scores. If none exceed 0.55 or answer "
        "seems incomplete, upgrade to `search_depth='advanced'` and "
        "max_results=6 **once only**.",
        "Never exceed two Tavily calls per user query.",
        # ── Answer construction ───────────────────────────────────────────
        "Extract no more than three key points per source.",
        "Cite every statement with URL slug in [brackets].",
        "Return exactly two sections:\n"
        "  1️⃣ **Executive Answer** (≤120 words)\n"
        "  2️⃣ **Sources & Rationale** (bullets, one per link)",
        # ── Tone & compliance ─────────────────────────────────────────────
        "Keep tone neutral and factual; no investment advice unless explicitly requested.",
        "If zero suitable sources remain after filtering, reply: "
        "`“No credible web evidence found within two passes.”`",
    ],
    show_tool_calls=True,               # transparency for debugging/logging
    markdown=True,
           # free cache layer (avoids duplicate cost)
)
