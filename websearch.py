import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.memory.v2.memory import Memory
from agno.models.google import Gemini
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage

load_dotenv()

# Set up SQLite memory storage
memory_db = SqliteMemoryDb(
    table_name="memories",
    db_file="tmp/memory.db"
)
memory = Memory(db=memory_db)

# Set up SQLite agent session storage
agent_storage = SqliteStorage(
    table_name="agent_sessions",
    db_file="tmp/agent_storage.db"
)

web_search_agent = Agent(
    name="WebScout",
    role="A fast web analyst who retrieves and summarizes real-time financial info",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools(cache_results=True)],
    instructions=[
        "Search the web using DuckDuckGo.",
        "Prefer financial and news sources like Bloomberg, Reuters, WSJ, etc.",
        "Summarize findings in 3 bullet points.",
        "Always include clickable source links at the end.",
        "Avoid speculation unless backed by a reputable source.",
    ],
    show_tool_calls=True,
    markdown=True,
    memory=memory,
    storage=agent_storage,
    enable_user_memories=True,
)
