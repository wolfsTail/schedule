from datetime import datetime

import pytest

from schedule.domain.model import (
    Availability,
    Location,
    Schedule,
    Ticket,
    Voyage,
)

# Тестовые данные для фикстур
@pytest.fixture
def test_origin():
    return Location("City A", (40.7128, -74.0060))

@pytest.fixture
def test_destination():
    return Location("City B", (34.0522, -118.2437))

@pytest.fixture
def test_voyage(test_origin, test_destination):
    return Voyage(
        voyage_id=1,
        dep_datetime_utc=datetime(2024, 12, 31, 10, 0),
        arr_datetime_utc=datetime(2024, 12, 31, 14, 0),
        origin=test_origin,
        destination=test_destination,
        marketing_number=123,
        vehicle_number="VH123",
    )

@pytest.fixture
def test_availability():
    return Availability(
        voyage_id=1,
        remaining_seats=50,
        bookings=10,
        is_active=True,
    )

@pytest.fixture
def test_ticket1():
    return Ticket(ticket_id=1, price=150.0, voyage_id=1, is_active=True)

@pytest.fixture
def test_ticket2():
    return Ticket(ticket_id=2, price=200.0, voyage_id=1, is_active=False)

@pytest.fixture
def test_schedule():
    return Schedule()

# Тест: добавление рейса
def test_add_voyage(test_schedule, test_voyage):
    test_schedule.add_voyage(test_voyage)
    assert len(test_schedule.voyages) == 1
    assert test_schedule.voyages[1].voyage_id == 1

# Тест: добавление доступности
def test_add_availability(test_schedule, test_voyage, test_availability):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_availability(test_availability)
    assert len(test_schedule.availability) == 1
    assert test_schedule.availability[1].remaining_seats == 50

# Тест: добавление билетов
def test_add_tickets(test_schedule, test_voyage, test_ticket1, test_ticket2):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_ticket(test_ticket1)
    test_schedule.add_ticket(test_ticket2)
    assert len(test_schedule.tickets) == 2
    assert test_schedule.tickets[1].price == 150.0
    assert not test_schedule.tickets[2].is_active

# Тест: получение расписания по дате
def test_get_schedule_by_date(test_schedule, test_voyage):
    test_schedule.add_voyage(test_voyage)
    result = test_schedule.get_schedule_by_date(
        datetime(2024, 12, 30), datetime(2025, 1, 1)
    )
    assert len(result) == 1
    assert result[0].voyage_id == 1

# Тест: получение доступности рейса
def test_get_voyage_availability(test_schedule, test_voyage, test_availability):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_availability(test_availability)
    avail = test_schedule.get_voyage_availability(1)
    assert avail.remaining_seats == 50

# Тест: получение билетов рейса
def test_get_tickets_by_voyage(test_schedule, test_voyage, test_ticket1, test_ticket2):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_ticket(test_ticket1)
    test_schedule.add_ticket(test_ticket2)
    tickets = test_schedule.get_tickets_by_voyage(1)
    assert len(tickets) == 2
    assert tickets[0].ticket_id == 1
    assert tickets[1].ticket_id == 2

# Тест: анализ загрузки рейса
def test_analyze_load(test_schedule, test_voyage, test_availability, test_ticket1, test_ticket2):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_availability(test_availability)
    test_schedule.add_ticket(test_ticket1)
    test_schedule.add_ticket(test_ticket2)
    load_info = test_schedule.analyze_load(1)
    assert load_info["total_seats"] == 60  # 50 remaining + 10 bookings
    assert load_info["sold_seats"] == 1    # Only ticket1 is active
    assert load_info["remaining_seats"] == 50

# Тест: представление класса
def test_schedule_repr(test_schedule, test_voyage, test_availability, test_ticket1, test_ticket2):
    test_schedule.add_voyage(test_voyage)
    test_schedule.add_availability(test_availability)
    test_schedule.add_ticket(test_ticket1)
    test_schedule.add_ticket(test_ticket2)
    repr_output = repr(test_schedule)
    assert "Schedule" in repr_output
    assert "1 voyages" in repr_output
    assert "1 availabilities" in repr_output
    assert "2 tickets" in repr_output
