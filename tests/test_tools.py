import pytest
from ai_assistant.tools import reserve_flight, reserve_hotel, reserve_restaurant, reserve_bus
from ai_assistant.utils import load_reservations, save_reservation, reset_reservations


@pytest.fixture
def log_file(mocker):
    file_name = "test_log.json"
    mocker.patch("ai_assistant.utils.SETTINGS.log_file", file_name)
    reset_reservations()

    yield

    log_reservations = load_reservations()
    assert len(log_reservations) == 1
    reset_reservations()


@pytest.mark.parametrize(
    "date, departure, destination",
    [
        ("2026-12-01", "La Paz", "Santa Cruz"),
        ("2026-12-23", "Cochabamba", "Santa Cruz"),
        ("2028-12-01", "La Paz", "Cochabamba"),
    ],
)
def test_reserve_flight(date, departure, destination, mocker, log_file):
    reservation = reserve_flight(date, departure, destination)
    assert reservation.trip_type == "FLIGHT"
    assert reservation.departure == departure
    assert reservation.destination == destination
    assert reservation.date.isoformat() == date
    assert reservation.cost >= 200 and reservation.cost <= 700


@pytest.mark.parametrize(
    "checkin_date, checkout_date, hotel_name, city",
    [
        ("2026-12-01", "2026-12-03", "Hotel A", "La Paz"),
        ("2026-12-23", "2026-12-25", "Hotel B", "Santa Cruz"),
        ("2028-12-01", "2028-12-03", "Hotel C", "Cochabamba"),
    ],
)
def test_reserve_hotel(checkin_date, checkout_date, hotel_name, city, mocker, log_file):
    reservation = reserve_hotel(checkin_date, checkout_date, hotel_name, city)
    assert reservation.hotel_name == hotel_name
    assert reservation.city == city
    assert reservation.checkin_date.isoformat() == checkin_date
    assert reservation.checkout_date.isoformat() == checkout_date
    assert reservation.cost >= 100 and reservation.cost <= 300


@pytest.mark.parametrize(
    "reservation_time, restaurant, city, dish",
    [
        ("2026-12-01T20:00:00", "Restaurant A", "La Paz", "Dish A"),
        ("2026-12-23T19:00:00", "Restaurant B", "Santa Cruz", "Dish B"),
        ("2028-12-01T21:00:00", "Restaurant C", "Cochabamba", "Dish C"),
    ],
)
def test_reserve_restaurant(reservation_time, restaurant, city, dish, mocker, log_file):
    reservation = reserve_restaurant(reservation_time, restaurant, city, dish)
    assert reservation.restaurant == restaurant
    assert reservation.city == city
    assert reservation.reservation_time.isoformat() == reservation_time
    assert reservation.dish == dish
    assert reservation.cost >= 10 and reservation.cost <= 50


@pytest.mark.parametrize(
    "date, departure, destination",
    [
        ("2026-12-01", "La Paz", "Santa Cruz"),
        ("2026-12-23", "Cochabamba", "Santa Cruz"),
        ("2028-12-01", "La Paz", "Cochabamba"),
    ],
)
def test_reserve_bus(date, departure, destination, mocker, log_file):
    reservation = reserve_bus(date, departure, destination)
    assert reservation.trip_type == "BUS"
    assert reservation.departure == departure
    assert reservation.destination == destination
    assert reservation.date.isoformat() == date
    assert reservation.cost >= 50 and reservation.cost <= 100


@pytest.mark.parametrize("date", ["2020-12-01", "2021-12-23", "2024-08-01"])
def test_reserve_flight_invalid_date(date):
    reset_reservations()

    with pytest.raises(ValueError):
        reserve_flight(date, "La Paz", "Santa Cruz")

    log_reservations = load_reservations()
    assert len(log_reservations) == 0


@pytest.mark.parametrize("reservation_time", ["2020-12-01T20:00:00", "2021-12-23T19:00:00", "2024-08-01T21:00:00"])
def test_reserve_restaurant_invalid_date(reservation_time):
    reset_reservations()

    with pytest.raises(ValueError):
        reserve_restaurant(reservation_time, "Restaurant A",
                           "La Paz", "Dish A")

    log_reservations = load_reservations()
    assert len(log_reservations) == 0


@pytest.mark.parametrize("checkin_date, checkout_date", [("2020-12-01", "2025-11-30"), ("2021-12-23", "2021-12-22"), ("2024-12-01", "2024-07-31")])
def test_reserve_hotel_invalid_dates(checkin_date, checkout_date):
    reset_reservations()

    with pytest.raises(ValueError):
        reserve_hotel(checkin_date, checkout_date, "Hotel A", "La Paz")

    log_reservations = load_reservations()
    assert len(log_reservations) == 0


@pytest.mark.parametrize("date", ["2020-12-01", "2021-12-23", "2024-08-01"])
def test_reserve_bus_invalid_date(date):
    reset_reservations()

    with pytest.raises(ValueError):
        reserve_bus(date, "La Paz", "Santa Cruz")

    log_reservations = load_reservations()
    assert len(log_reservations) == 0
