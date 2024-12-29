from datetime import datetime

from model import (
    Availability,
    Location,
    Schedule,
    Ticket,
    Voyage,
)


origin = Location("City A", (40.7128, -74.0060))
destination = Location("City B", (34.0522, -118.2437))

voyage = Voyage(
    voyage_id=1,
    dep_datetime_utc=datetime(2024, 12, 31, 10, 0),
    arr_datetime_utc=datetime(2024, 12, 31, 14, 0),
    origin=origin,
    destination=destination,
    marketing_number=123,
    vehicle_number="VH123",
)

availability = Availability(
    voyage_id=1,
    remaining_seats=50,
    bookings=10,
    is_active=True,
)

ticket1 = Ticket(ticket_id=1, price=150.0, voyage_id=1, is_active=True)
ticket2 = Ticket(ticket_id=2, price=200.0, voyage_id=1, is_active=False)

# Создание объекта Schedule
schedule = Schedule()

# Тест: добавление рейса
schedule.add_voyage(voyage)
assert len(schedule.voyages) == 1
assert schedule.voyages[1].voyage_id == 1

# Тест: добавление доступности
schedule.add_availability(availability)
assert len(schedule.availability) == 1
assert schedule.availability[1].remaining_seats == 50

# Тест: добавление билетов
schedule.add_ticket(ticket1)
schedule.add_ticket(ticket2)
assert len(schedule.tickets) == 2
assert schedule.tickets[1].price == 150.0
assert schedule.tickets[2].is_active is False

# Тест: получение расписания по дате
result = schedule.get_schedule_by_date(
    datetime(2024, 12, 30), datetime(2025, 1, 1)
)
assert len(result) == 1
assert result[0].voyage_id == 1

# Тест: получение доступности рейса
avail = schedule.get_voyage_availability(1)
assert avail.remaining_seats == 50

# Тест: получение билетов рейса
tickets = schedule.get_tickets_by_voyage(1)
assert len(tickets) == 2
assert tickets[0].ticket_id == 1
assert tickets[1].ticket_id == 2

# Тест: анализ загрузки рейса
load_info = schedule.analyze_load(1)
assert load_info["total_seats"] == 60  # 50 remaining + 10 bookings
assert load_info["sold_seats"] == 1    # Only ticket1 is active
assert load_info["remaining_seats"] == 50

# Тест: представление класса
repr_output = repr(schedule)
assert "Schedule" in repr_output
assert "1 voyages" in repr_output
assert "1 availabilities" in repr_output
assert "2 tickets" in repr_output

print("Все тесты успешно пройдены!")