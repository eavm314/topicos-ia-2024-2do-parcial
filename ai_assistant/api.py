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


def format_notes(notes: list[str]) -> str:
    formated_notes = ""
    for note in notes:
        formated_notes += f"- {note}\n"
    return formated_notes


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"Recommend me some cities in Bolivia to visit with the following notes: {notes}."
    return AgentAPIResponse(status="OK", agent_response=str(agent.query(prompt)))


@app.get("/recommendations/places")
def recommend_places(
    city: str, notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = format_notes(notes)
    prompt = recommend_cities_prompt.format(
        notes=formated_notes,
        city=city,
        field="places",
        description="places to visit in the city and their descriptions"
    )
    return AgentAPIResponse(status="OK", agent_response=str(agent.query(prompt)))


@app.get("/recommendations/hotels")
def recommend_hotels(
    city: str, notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = format_notes(notes)
    prompt = recommend_cities_prompt.format(
        notes=formated_notes,
        city=city,
        field="hotels",
        description="main hotels in the city and their locations"
    )
    return AgentAPIResponse(status="OK", agent_response=str(agent.query(prompt)))


@app.get("/recommendations/activities")
def recommend_activities(
    city: str, notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = format_notes(notes)
    prompt = recommend_cities_prompt.format(
        notes=formated_notes,
        city=city,
        field="activities",
        description="main activities to do in the city"
    )
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
