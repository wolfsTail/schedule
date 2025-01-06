from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    title: str
    coordinates: tuple[float, float]


@dataclass
class Ticket:
    ticket_id: int | None
    price: float
    voyage_id: int
    is_active: bool


class Voyage:
    def __init__(
        self,
        voyage_id: int | None,
        dep_datetime_utc: datetime,
        arr_datetime_utc: datetime,
        origin: Location,
        destination: Location,
        marketing_number: int,
        vehicle_number: str,
    ):
        self.voyage_id = voyage_id
        self.dep_datetime_utc = dep_datetime_utc
        self.arr_datetime_utc = arr_datetime_utc
        self.origin = origin
        self.destination = destination
        self.marketing_number = marketing_number
        self.vehicle_number = vehicle_number

    def __repr__(self):
        return (
            f"Voyage (id={self.voyage_id!r}, "
            f"{self.arr_datetime_utc!r}, origin={self.origin!r}, destination={self.destination!r},"
            f"marketing_number={self.marketing_number!r}, vehicle_number={self.vehicle_number!r})"
        )
    
    def voyage_length(self):
        return self.arr_datetime_utc - self.dep_datetime_utc


class Availability:
    def __init__(
        self,
        voyage_id: int,
        remaining_seats: int,
        bookings: int,
        is_active: bool,
    ):
        self.voyage_id = voyage_id
        self.remaining_seats = remaining_seats
        self.bookings = bookings
        self.is_active = is_active
    
    def __repr__(self):
        return (
            f"Availability (voyage_id={self.voyage_id!r}, "
            f"remaining_seats={self.remaining_seats!r}, bookings={self.bookings!r}, "
            f"is_active={self.is_active!r})"
        )


from datetime import datetime, date
from typing import Optional

from datetime import datetime, date
from typing import Optional


class Schedule:
    def __init__(self, schedule_date: Optional[date] = None):
        self.schedule_date: Optional[date] = schedule_date
        self.voyages: dict[int, Voyage] = {}
        self.availability: dict[int, Availability] = {}
        self.tickets: dict[int, Ticket] = {}

    def set_schedule_date(self, schedule_date: date):
        self.schedule_date = schedule_date

    def add_voyage(self, voyage: Voyage):
        if self.schedule_date and voyage.dep_datetime_utc.date() != self.schedule_date:
            raise ValueError(
                f"Voyage date {voyage.dep_datetime_utc.date()} does not match schedule date {self.schedule_date}."
            )
        self.voyages[voyage.voyage_id] = voyage

    def add_availability(self, availability: Availability):
        if availability.voyage_id not in self.voyages:
            raise ValueError(f"Voyage with ID {availability.voyage_id} not found.")
        self.availability[availability.voyage_id] = availability

    def add_ticket(self, ticket: Ticket):
        if ticket.voyage_id not in self.voyages:
            raise ValueError(f"Voyage with ID {ticket.voyage_id} not found.")
        self.tickets[ticket.ticket_id] = ticket

    def get_schedule_by_date(self, start_date: datetime, end_date: datetime) -> list[
        Voyage]:
        return [
            voyage for voyage in self.voyages.values()
            if start_date <= voyage.dep_datetime_utc <= end_date
        ]

    def get_voyage_availability(self, voyage_id: int) -> Optional[Availability]:
        return self.availability.get(voyage_id, None)

    def get_tickets_by_voyage(self, voyage_id: int) -> list[Ticket]:
        return [ticket for ticket in self.tickets.values() if
                ticket.voyage_id == voyage_id]

    def analyze_load(self, voyage_id: int) -> dict[str, int]:
        availability = self.get_voyage_availability(voyage_id)
        if not availability:
            raise ValueError(f"Availability for voyage ID {voyage_id} not found.")

        tickets = self.get_tickets_by_voyage(voyage_id)
        sold_seats = len([ticket for ticket in tickets if ticket.is_active])

        return {
            "total_seats": availability.remaining_seats + availability.bookings,
            "sold_seats": sold_seats,
            "remaining_seats": availability.remaining_seats,
        }

    def get_schedule_summary(self) -> dict[str, int]:
        total_seats = sum(
            availability.remaining_seats + availability.bookings
            for availability in self.availability.values()
        )
        sold_seats = sum(
            len([ticket for ticket in self.get_tickets_by_voyage(voyage_id) if
                 ticket.is_active])
            for voyage_id in self.voyages
        )
        return {
            "total_voyages": len(self.voyages),
            "total_tickets": len(self.tickets),
            "total_seats": total_seats,
            "sold_seats": sold_seats,
        }

    def __repr__(self):
        return (
            f"Schedule for {self.schedule_date}: {len(self.voyages)} voyages, "
            f"{len(self.availability)} availabilities, {len(self.tickets)} tickets"
        )

