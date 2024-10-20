from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse
from ai_assistant.prompts import agent_prompt_tpl, recommend_cities_prompt, travel_report_prompt
from functools import cache

@cache
def get_agent() -> ReActAgent:
    return TravelAgent(agent_prompt_tpl).get_agent()


app = FastAPI(title="AI Travel Assistant Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = ""
    for note in notes:
        formated_notes += f"- {note}\n"
    prompt = recommend_cities_prompt.format(notes=formated_notes)
    return AgentAPIResponse(status="OK", agent_response=str(agent.query(prompt)))

@app.get("/report")
def get_travel_report(
    notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = ""
    for note in notes:
        formated_notes += f"- {note}\n"
    prompt = travel_report_prompt.format(notes=formated_notes)
    return AgentAPIResponse(status="OK", agent_response=str(agent.query(prompt)))