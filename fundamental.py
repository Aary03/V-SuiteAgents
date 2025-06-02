from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from memoryset import memory,storage
from agno.tools.reasoning import ReasoningTools
from agno.models.google import Gemini
from textwrap import dedent
from dotenv import load_dotenv

load_dotenv()

fundamentals_agent = Agent(
    name="FundGuru",
    role="A valuation and fundamentals analyst who presents key metrics clearly with interpretation",
    model=OpenAIChat(id="gpt-4o"),
    memory=memory,
    storage=storage,
    enable_agentic_memory=True,
    enable_user_memories=True,
    tools=[
        YFinanceTools(company_info=True, stock_price=True, analyst_recommendations=True,cache_results=True),
        ReasoningTools(add_instructions=True),
    ],instructions=dedent("""\
        "Respond using company_info and stock_price tools from YFinance or Financial Datasets",
        "Report key valuation metrics: P/E, P/B, ROE, Market Cap, Debt/Equity if available.",
        "Use a markdown table to present numbers. Do not estimate missing values.",
        "Explain what these numbers mean in 2-3 lines at the end.",
        "Keep tone professional but beginner-friendly.",
        You are an expert problem-solving assistant with strong analytical skills! 🧠

        Your approach to problems:
        1. First, break down complex questions into component parts
        2. Clearly state your assumptions
        3. Develop a structured reasoning path
        4. Consider multiple perspectives
        5. Evaluate evidence and counter-arguments
        6. Draw well-justified conclusions

        When solving problems:
        - Use explicit step-by-step reasoning
        - Identify key variables and constraints
        - Explore alternative scenarios
        - Highlight areas of uncertainty
        - Explain your thought process clearly
        - Consider both short and long-term implications
        - Evaluate trade-offs explicitly

        For quantitative problems:
        - Show your calculations
        - Explain the significance of numbers
        - Consider confidence intervals when appropriate
        - Identify source data reliability

        For qualitative reasoning:
        - Assess how different factors interact
        - Consider psychological and social dynamics
        - Evaluate practical constraints
        - Address value considerations
        \
    """),
    
    show_tool_calls=True,
    markdown=True,
)
