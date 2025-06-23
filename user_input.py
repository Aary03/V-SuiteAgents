from agno.agent import Agent
 
# from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
 
from agno.models.openai import OpenAIResponses
 
load_dotenv()
 
agentwebopen = Agent(
    model=OpenAIResponses(id="gpt-4o"),
    tools=[{"type": "web_search_preview"}],
    instructions="When invoked, run an immediate web search (prefer ≤30-day recency). "
        "Return:\n"
        "• A 1-sentence headline with the fresh takeaway.\n"
        "• A bullet list (max 5 bullets, ≤15 words each) of key facts.\n"
        "• Up to 3 source links as Markdown footnotes.\n"
        "Avoid paywalled results, skip ads, and finish in <250 tokens.",
    markdown=True,
)
# agentwebopen.print_response(
#     "What is the latest news on the stock market?",
#     markdown=True,
#     show_tool_calls=True,
# )
 
 
# agentexa = Agent(model=OpenAIChat(id="gpt-4o"),
#     tools=[ExaTools(start_published_date="2025-01-01",
#         end_published_date="2025-12-31",
#         text_length_limit=1000,
#     )],
#     show_tool_calls=True,
# )