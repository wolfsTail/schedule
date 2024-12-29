from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    title: str
    coordinates: tuple[float, float]


@dataclass
class Ticket:
    ticket_id: int
    price: float
    voyage_id: int
    is_active: bool


class Voyage:
    def __init__(
        self,
        voyage_id: int,
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
