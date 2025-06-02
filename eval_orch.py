from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from orch import valura_team
from typing import Optional
from websearch import web_search_agent

evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=web_search_agent,
    input="What is the capital of France?",
    expected_output="Paris",
    additional_guidelines="The answer should be concise and correct.",
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8 