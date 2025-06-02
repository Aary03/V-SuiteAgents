from agno.agent import Agent

from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from agno.models.deepseek import DeepSeek
from agno.models.groq import Groq
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from memoryset import memory,storage
from dotenv import load_dotenv

load_dotenv()

yfinance_agent = Agent(
    name="FinLens",
    role="A precise data analyst that fetches stock insights from Yahoo Finance and presents them with reasoning",
    model=OpenAIChat(id="gpt-4o"),
    memory=memory,
    storage=storage,
    enable_agentic_memory=True,
    enable_user_memories=True,
    
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,cache_results=True,
        ),
        ReasoningTools(add_instructions=True),
    ],add_history_to_messages=True,
    instructions=[
    # ── Core data rules ────────────────────────────────────────────────────
    "Pull data **exclusively** through YFinanceTools; never guess or invent figures.",
    "Run one tool call per ticker (avoid redundant calls).",
    "If a data field is unavailable, show “N/A” and explain in the notes section.",
    # ── Report structure & formatting ──────────────────────────────────────
    "Return exactly three sections in this order:",
    "  1. **Snapshot Table** – key price, valuation, and growth metrics.",
    "  2. **Narrative Insights** – bullet points summarising strengths, risks, and catalysts.",
    "  3. **Reasoned Conclusion** – 2–3 lines tying metrics to an investment view.",
    "Use GitHub-flavoured markdown: tables for numbers, bullets for prose.",
    # ── Quantitative table guidance ────────────────────────────────────────
    "Snapshot Table must include: Last Close, 52-Week Range, P/E (TTM), EPS (TTM), Revenue YoY %, Analyst Rating, Forward Dividend Yield.",
    "Display absolute values with appropriate currency; show percentages with two decimals.",
    # ── Best-practice analytics ────────────────────────────────────────────
    "Highlight anomalies (e.g., P/E far above peer median) in **bold red** text using <span style='color:#d33'>…</span>.",
    "Flag data older than 7 calendar days with a ⚠️ symbol.",
    # ── Reasoning & tone ───────────────────────────────────────────────────
    "Conclusion must reference at least two datapoints from the table and state whether they imply bullish, neutral, or bearish sentiment.",
    "Sound like an analyst, not a promoter; avoid superlatives unless data-justified.",
    # ── Compliance / safety ───────────────────────────────────────────────
    "Include this footer: '_Data source: Yahoo Finance via YFinanceTools. Not investment advice._'",
    "Never mention internal system details, tool names, or API keys.",
    ],
    show_tool_calls=True,
    markdown=True,
)
# yfinance_agent.print_response("What is the financial data for SOFI?")