# memory_setup.py
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.models.openai import OpenAIChat

db_file = "tmp/agentic_memory.db"

memory = Memory(
    model=OpenAIChat(id="gpt-4o"),
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
)
storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)