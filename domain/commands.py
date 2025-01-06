from dataclasses import dataclass
from datetime import date, datetime
from typing import Any


class Command:
    metadata: dict[str, Any] = None


@dataclass
class CreateLocationCommand(Command):
    title: str
    latitude: float
    longitude: float

@dataclass
class UpdateLocationCommand(Command):
    location_id: int
    title: str = None
    latitude: float = None
    longitude: float = None


@dataclass
class DeleteLocationCommand(Command):
    location_id: int


class CreateVoyageCommand(Command):
    dep_datetime_utc: datetime
    arr_datetime_utc: datetime
    origin_id: int
    destination_id: int
    marketing_number: int
    vehicle_number: str

@dataclass
class UpdateVoyageCommand(Command):
    voyage_id: int
    dep_datetime_utc: datetime = None
    arr_datetime_utc: datetime = None

@dataclass
class DeleteVoyageCommand(Command):
    voyage_id: int


@dataclass
class CreateTicketCommand(Command):
    voyage_id: int
    price: float
    is_active: bool = True

@dataclass
class UpdateTicketStatusCommand(Command):
    ticket_id: int
    is_active: bool

@dataclass
class DeleteTicketCommand(Command):
    ticket_id: int

@dataclass
class SetAvailabilityCommand(Command):
    voyage_id: int
    remaining_seats: int
    bookings: int
    is_active: bool = True

@dataclass
class UpdateAvailabilityCommand(Command):
    voyage_id: int
    remaining_seats: int = None
    bookings: int = None
    is_active: bool = None


@dataclass
class CreateScheduleCommand(Command):
    schedule_date: date

@dataclass
class AddVoyageToScheduleCommand(Command):
    schedule_id: int
    dep_datetime_utc: datetime
    arr_datetime_utc: datetime
    origin_id: int
    destination_id: int
    marketing_number: int
    vehicle_number: str

@dataclass
class DeleteScheduleCommand(Command):
    schedule_id: int
