from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, datetime


class TripType(str, Enum):
    flight = "FLIGHT"
    bus = "BUS"


class TripReservation(BaseModel):
    trip_type: TripType
    date: date
    departure: str
    destination: str
    cost: int


class HotelReservation(BaseModel):
    checkin_date: date
    checkout_date: date
    hotel_name: str
    city: str
    cost: int


class RestaurantReservation(BaseModel):
    reservation_time: datetime
    restaurant: str
    city: str
    dish: str
    cost: int


class APIResponse(BaseModel):
    status: str
    message: str

class AgentAPIResponse(APIResponse):
    agent_response: str
    timestamp: datetime = Field(default_factory=datetime.now)

