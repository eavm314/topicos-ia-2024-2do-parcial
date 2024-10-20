from random import randint
from datetime import date, datetime, time
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
from ai_assistant.models import (
    TripReservation,
    TripType,
    HotelReservation,
    RestaurantReservation,
)
from ai_assistant.utils import save_reservation, load_reservations

SETTINGS = get_agent_settings()

travel_guide_tool = QueryEngineTool(
    query_engine=TravelGuideRAG(
        store_path=SETTINGS.travel_guide_store_path,
        data_dir=SETTINGS.travel_guide_data_path,
        qa_prompt_tpl=travel_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="travel_guide", description=travel_guide_description, return_direct=False
    ),
)


# Tool functions
def reserve_flight(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    This function reserves a flight from a departure location to a destination on a given date.
    Args:
        - date_str (str): The date of the flight in ISO format.
        - departure (str): The departure location.
        - destination (str): The destination location.
    Notes:
        - The cost of the flight is randomly generated between 200 and 700.
        - If the reservation is successful, the reservation details are saved.
    Returns:
        - TripReservation: The reservation details.
    Raises:
        - ValueError: If the flight date is in the past.
    """
    
    flight_date = date.fromisoformat(date_str)
    if flight_date < date.today():
        raise ValueError("Invalid flight date. The date cannot be in the past.")
    
    print(
        f"Making flight reservation from {departure} to {destination} on date: {date_str}"
    )
    reservation = TripReservation(
        trip_type=TripType.flight,
        departure=departure,
        destination=destination,
        date=flight_date,
        cost=randint(200, 700),
    )

    save_reservation(reservation)
    return reservation

def reserve_hotel(
    checkin_date_str: str, checkout_date_str: str, hotel_name: str, city: str
) -> HotelReservation:
    """
    This function reserves a hotel stay at a specific hotel in a city.
    Args:
        - checkin_date_str (str): The check-in date in ISO format.
        - checkout_date_str (str): The check-out date in ISO format.
        - hotel_name (str): The name of the hotel.
        - city (str): The city where the hotel is located.
    Notes:
        - The cost of the hotel reservation is randomly generated between 100 and 300.
        - If the reservation is successful, the reservation details are saved.
    Returns:
        - HotelReservation: The reservation details.
    Raises:
        - ValueError: If the check-in date is in the past or the check-out date is before the check-in date.
    """
    checkin_date = date.fromisoformat(checkin_date_str)
    checkout_date = date.fromisoformat(checkout_date_str)
    if checkin_date < date.today():
        raise ValueError("Invalid check-in date. The date cannot be in the past.")
    if checkin_date >= checkout_date:
        raise ValueError("Invalid check-in and check-out dates. Check-out date should be after check-in date.")
    
    print(f"Making hotel reservation at {hotel_name} in {city}")
    reservation = HotelReservation(
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        hotel_name=hotel_name,
        city=city,
        cost=randint(100, 300),
    )

    save_reservation(reservation)
    return reservation

def reserve_bus(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    This function reserves a bus trip from a departure location to a destination on a given date.
    Args:
        - date_str (str): The date of the trip in ISO format.
        - departure (str): The departure location.
        - destination (str): The destination location.
    Notes:
        - The cost of the bus trip is randomly generated between 50 and 100.
        - If the reservation is successful, the reservation details are saved.
    Returns:
        - TripReservation: The reservation details.
    Raises:
        - ValueError: If the trip date is in the past.
    """
    trip_date = date.fromisoformat(date_str)
    if trip_date < date.today():
        raise ValueError("Invalid trip date. The date cannot be in the past.")
    
    print(f"Making bus reservation from {departure} to {destination} on date: {date_str}")
    reservation = TripReservation(
        trip_type=TripType.bus,
        departure=departure,
        destination=destination,
        date=trip_date,
        cost=randint(50, 100),
    )

    save_reservation(reservation)
    return reservation

def reserve_restaurant(
    reservation_time_str: str, restaurant: str, city: str, dish: str
) -> RestaurantReservation:
    """
    This function makes a restaurant reservation at a specific restaurant in a city for a given dish.
    Args:
        - reservation_time_str (str): The reservation time in ISO format.
        - restaurant (str): The name of the restaurant.
        - city (str): The city where the restaurant is located.
        - dish (str): The dish to be reserved.
    Notes:
        - The cost of the restaurant reservation is randomly generated between 10 and 50.
        - If the reservation is successful, the reservation details are saved.
    Returns:
        - RestaurantReservation: The reservation details.
    """
    reservation_time = datetime.fromisoformat(reservation_time_str)
    if reservation_time < datetime.now():
        raise ValueError("Invalid reservation time. The time cannot be in the past.")
    
    print(f"Making restaurant reservation at {restaurant} in {city} for {dish} at {reservation_time_str}")
    reservation = RestaurantReservation(
        reservation_time=reservation_time,
        restaurant=restaurant,
        city=city,
        dish=dish,
        cost=randint(10, 50),
    )

    save_reservation(reservation)
    return reservation

def get_current_date() -> str:
    """
    This function returns the current date in ISO format.
    Returns:
        - str: The current date in ISO format.
    """
    return date.today().isoformat()

def travel_report() -> tuple[list, int]:
    """
    This function loads the saved reservations from the log file.
    Returns:
        - list: The list of saved reservations.
        - int: The total cost.
    Notes:
        - The reservations could be of type TripReservation, HotelReservation, or RestaurantReservation.
        - The dates and times are in ISO format.
        - The costs are in Bolivianos (BOB).
    """
    reservations = load_reservations()
    total_cost = sum(reservation["cost"] for reservation in reservations)
    return reservations, total_cost


flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)
hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)
bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)
restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)
get_current_date_tool = FunctionTool.from_defaults(fn=get_current_date, return_direct=False)
travel_report_tool = FunctionTool.from_defaults(fn=travel_report, return_direct=False)