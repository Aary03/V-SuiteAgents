import os
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True)],
    instructions = [
        "Use tables to display data.",
        "Only include the table in your response. No other text.",
    ],
    markdown=True
)

