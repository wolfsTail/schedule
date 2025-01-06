from sqlalchemy import Table, MetaData, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import mapper, relationship, clear_mappers
from schedule import domain


metadata = MetaData()

schedules = Table(
    "schedules",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("schedule_date", Date, nullable=False, unique=True),
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
)

voyages = Table(
    "voyages",
    metadata,
    Column("voyage_id", Integer, primary_key=True, autoincrement=True),
    Column("dep_datetime_utc", DateTime, nullable=False),
    Column("arr_datetime_utc", DateTime, nullable=False),
    Column("origin_id", ForeignKey("locations.id"), nullable=False),
    Column("destination_id", ForeignKey("locations.id"), nullable=False),
    Column("marketing_number", Integer, nullable=False),
    Column("vehicle_number", String(255), nullable=False),
    Column("schedule_id", ForeignKey("schedules.id"), nullable=False),
)

tickets = Table(
    "tickets",
    metadata,
    Column("ticket_id", Integer, primary_key=True, autoincrement=True),
    Column("price", Float, nullable=False),
    Column("voyage_id", ForeignKey("voyages.voyage_id"), nullable=False),
    Column("is_active", Boolean, default=True),
)

availability = Table(
    "availability",
    metadata,
    Column("voyage_id", ForeignKey("voyages.voyage_id"), primary_key=True),
    Column("remaining_seats", Integer, nullable=False),
    Column("bookings", Integer, nullable=False),
    Column("is_active", Boolean, default=True),
)


def start_mappers():
    clear_mappers()

    mapper(
        domain.Schedule,
        schedules,
        properties={
            "voyages": relationship(
                domain.Voyage, back_populates="schedule", cascade="all, delete-orphan"
            ),
        },
    )

    mapper(
        domain.Location,
        locations,
    )

    mapper(
        domain.Voyage,
        voyages,
        properties={
            "origin": relationship(domain.Location, foreign_keys=[voyages.c.origin_id]),
            "destination": relationship(domain.Location, foreign_keys=[voyages.c.destination_id]),
            "tickets": relationship(domain.Ticket, back_populates="voyage"),
            "availability": relationship(domain.Availability, back_populates="voyage", uselist=False),
            "schedule": relationship(domain.Schedule, back_populates="voyages"),
        },
    )

    mapper(
        domain.Ticket,
        tickets,
        properties={
            "voyage": relationship(domain.Voyage, back_populates="tickets"),
        },
    )

    mapper(
        domain.Availability,
        availability,
        properties={
            "voyage": relationship(domain.Voyage, back_populates="availability"),
        },
    )
