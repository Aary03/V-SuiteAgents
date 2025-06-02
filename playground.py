from dotenv import load_dotenv
load_dotenv()

from agno.playground import Playground, serve_playground_app

# Import your agents and team
from websearch import web_search_agent
from yfinanceagent import yfinance_agent
from fundamental import fundamentals_agent
from masterfinance import agent
from masterwebsearch import wavily
from orch import valura_team

# List all agents and teams you want in the UI
app = Playground(
    agents=[
        web_search_agent,
        yfinance_agent,
        fundamentals_agent,agent,wavily
        
         
    ]
).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True) 