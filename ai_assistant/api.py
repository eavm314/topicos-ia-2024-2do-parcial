from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse


def get_agent() -> ReActAgent:
    return TravelAgent().get_agent()


app = FastAPI(title="AI Travel Assistant Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
