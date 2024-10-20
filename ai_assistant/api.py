from fastapi import FastAPI, Depends, Query, HTTPException
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse, APIResponse
from ai_assistant.prompts import agent_prompt_tpl, recommend_cities_prompt, travel_report_prompt
from ai_assistant.tools import reserve_bus, reserve_flight, reserve_hotel, reserve_restaurant
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
    return AgentAPIResponse(
        status="OK", 
        message="Recommendations obtained successfully", 
        agent_response=str(agent.query(prompt))
    )


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
    return AgentAPIResponse(
        status="OK", 
        message="Recommendations obtained successfully", 
        agent_response=str(agent.query(prompt))
    )


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
    return AgentAPIResponse(
        status="OK", 
        message="Recommendations obtained successfully", 
        agent_response=str(agent.query(prompt))
    )


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
    return AgentAPIResponse(
        status="OK", 
        message="Recommendations obtained successfully", 
        agent_response=str(agent.query(prompt))
    )


@app.get("/report")
def get_travel_report(
    notes: list[str] = Query([]), agent: ReActAgent = Depends(get_agent)
):
    formated_notes = ""
    for note in notes:
        formated_notes += f"- {note}\n"
    prompt = travel_report_prompt.format(notes=formated_notes)
    return AgentAPIResponse(
        status="OK", 
        message="Travel report obtained successfully",
        agent_response=str(agent.query(prompt))
    )


@app.post("/reserve/flight")
def flight_reservation(date: str, departure: str, destination: str):
    try:
        reserve_flight(date, departure, destination)
        return APIResponse(
            status="OK", 
            message="Flight reservation successful"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/reserve/bus")
def bus_reservation(date: str, departure: str, destination: str):
    try:
        reserve_bus(date, departure, destination)
        return APIResponse(
            status="OK", 
            message="Bus reservation successful"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/reserve/hotel")
def hotel_reservation(chekin_date: str, chekout_date: str, hotel_name: str, city: str):
    try:
        reserve_hotel(chekin_date, chekout_date, hotel_name, city)
        return APIResponse(
            status="OK", 
            message="Hotel reservation successful"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/reserve/restaurant")
def restaurant_reservation(reservation_time: str, restaurant: str, city: str, dish: str):
    try:
        reserve_restaurant(reservation_time, restaurant, city, dish)
        return APIResponse(
            status="OK", 
            message="Restaurant reservation successful"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))