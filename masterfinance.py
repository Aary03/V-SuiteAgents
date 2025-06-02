from agno.agent import Agent,RunResponse
from agno.tools.financial_datasets import FinancialDatasetsTools
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Financial Data Agent",
    tools=[
        FinancialDatasetsTools(),  # For accessing financial data
    ],
    description="You are a financial data specialist that helps analyze financial information for stocks and cryptocurrencies.",
    instructions=[
        "When given a financial query:",
        "1. Use appropriate Financial Datasets methods based on the query type",
        "2. Format financial data clearly and highlight key metrics",
        "3. For financial statements, compare important metrics with previous periods when relevant",
        "4. Calculate growth rates and trends when appropriate",
        "5. Handle errors gracefully and provide meaningful feedback",
    ],
    markdown=True,
    show_tool_calls=True,
)
