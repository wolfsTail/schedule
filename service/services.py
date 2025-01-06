from datetime import date

from schedule import domain


class BaseService:
    def __init__(self, session):
        self.session = session


class LocationService(BaseService):
    def __init__(self, session, location_repo):
        super().__init__(session)
        self.location_repo = location_repo

    def create_location(self, title, latitude, longitude):
        location = domain.Location(
            title=title,
            coordinates=(latitude, longitude)
        )
        self.location_repo.add(location)
        self.session.commit()
        return location

    def get_location(self, location_id):
        location = self.location_repo.get(location_id)
        if not location:
            raise ValueError(f"Location with ID {location_id} not found")
        return location

    def list_locations(self):
        return self.location_repo.list()

    def update_location(self, location_id, title=None, latitude=None, longitude=None):
        location = self.get_location(location_id)

        if title:
            location.title = title
        if latitude is not None and longitude is not None:
            location.coordinates = (latitude, longitude)

        self.session.commit()
        return location

    def delete_location(self, location_id):
        location = self.get_location(location_id)
        self.session.delete(location)
        self.session.commit()
        return location


class VoyageService(BaseService):
    def __init__(self, session, voyage_repo, location_repo):
        super().__init__(session)
        self.voyage_repo = voyage_repo
        self.location_repo = location_repo

    def create_voyage(
            self,
            dep_datetime_utc,
            arr_datetime_utc,
            origin_id,
            destination_id,
            marketing_number,
            vehicle_number
    ):
        origin = self.location_repo.get(origin_id)
        destination = self.location_repo.get(destination_id)

        if not origin or not destination:
            raise ValueError("Invalid origin or destination ID")

        voyage = domain.Voyage(
            voyage_id=None,
            dep_datetime_utc=dep_datetime_utc,
            arr_datetime_utc=arr_datetime_utc,
            origin=origin,
            destination=destination,
            marketing_number=marketing_number,
            vehicle_number=vehicle_number,
        )
        self.voyage_repo.add(voyage)
        self.session.commit()
        return voyage

    def get_voyages_by_origin(self, origin_id):
        return self.voyage_repo.get_by_origin(origin_id)

class TicketService(BaseService):
    def __init__(self, session, ticket_repo, voyage_repo):
        super().__init__(session)
        self.ticket_repo = ticket_repo
        self.voyage_repo = voyage_repo

    def create_ticket(self, voyage_id, price, is_active=True):
        voyage = self.voyage_repo.get(voyage_id)

        if not voyage:
            raise ValueError("Invalid voyage ID")

        ticket = domain.Ticket(
            ticket_id=None,
            price=price,
            voyage_id=voyage_id,
            is_active=is_active,
        )
        self.ticket_repo.add(ticket)
        self.session.commit()
        return ticket

    def get_active_tickets(self, voyage_id):
        return self.ticket_repo.get_active_tickets(voyage_id)

class AvailabilityService(BaseService):
    def __init__(self, session, availability_repo, voyage_repo):
        super().__init__(session)
        self.availability_repo = availability_repo
        self.voyage_repo = voyage_repo

    def set_availability(self, voyage_id, remaining_seats, bookings, is_active=True):
        voyage = self.voyage_repo.get(voyage_id)

        if not voyage:
            raise ValueError("Invalid voyage ID")

        availability = domain.Availability(
            voyage_id=voyage_id,
            remaining_seats=remaining_seats,
            bookings=bookings,
            is_active=is_active,
        )
        self.availability_repo.add(availability)
        self.session.commit()
        return availability

    def get_availability(self, voyage_id):
        return self.availability_repo.get_by_voyage(voyage_id)


class ScheduleService(BaseService):
    def __init__(self, session, schedule_repo, voyage_repo, location_repo, ticket_repo,
                 availability_repo):
        super().__init__(session)
        self.schedule_repo = schedule_repo
        self.voyage_repo = voyage_repo
        self.location_repo = location_repo
        self.ticket_repo = ticket_repo
        self.availability_repo = availability_repo

    def create_schedule(self, schedule_date: date):
        if self.schedule_repo.get_by_date(schedule_date):
            raise ValueError(f"Schedule for date {schedule_date} already exists.")

        schedule = domain.Schedule(schedule_date=schedule_date)
        self.schedule_repo.add(schedule)
        self.session.commit()
        return schedule

    def add_voyage_to_schedule(
            self, schedule_id, dep_datetime_utc, arr_datetime_utc, origin_id,
            destination_id, marketing_number, vehicle_number
    ):
        schedule = self.schedule_repo.get(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found.")

        origin = self.location_repo.get(origin_id)
        destination = self.location_repo.get(destination_id)

        if not origin or not destination:
            raise ValueError("Invalid origin or destination ID.")

        voyage = domain.Voyage(
            voyage_id=None,
            dep_datetime_utc=dep_datetime_utc,
            arr_datetime_utc=arr_datetime_utc,
            origin=origin,
            destination=destination,
            marketing_number=marketing_number,
            vehicle_number=vehicle_number,
            schedule=schedule,
        )
        self.voyage_repo.add(voyage)
        self.session.commit()
        return voyage

    def set_availability(self, voyage_id, remaining_seats, bookings, is_active=True):
        voyage = self.voyage_repo.get(voyage_id)
        if not voyage:
            raise ValueError(f"Voyage with ID {voyage_id} not found.")

        availability = domain.Availability(
            voyage_id=voyage_id,
            remaining_seats=remaining_seats,
            bookings=bookings,
            is_active=is_active,
        )
        self.availability_repo.add(availability)
        self.session.commit()
        return availability

    def add_tickets(self, voyage_id, tickets):
        voyage = self.voyage_repo.get(voyage_id)
        if not voyage:
            raise ValueError(f"Voyage with ID {voyage_id} not found.")

        for ticket_data in tickets:
            ticket = domain.Ticket(
                ticket_id=None,
                price=ticket_data["price"],
                voyage_id=voyage_id,
                is_active=ticket_data.get("is_active", True),
            )
            self.ticket_repo.add(ticket)

        self.session.commit()

    def get_schedule_by_date(self, schedule_date: date):
        schedule = self.schedule_repo.get_by_date(schedule_date)
        if not schedule:
            raise ValueError(f"No schedule found for date {schedule_date}.")
        return schedule

    def get_schedule_summary(self, schedule_date: date):
        schedule = self.get_schedule_by_date(schedule_date)
        voyages = schedule.voyages
        summary = {
            "schedule_date": schedule.schedule_date,
            "total_voyages": len(voyages),
            "total_tickets": sum(
                len(self.ticket_repo.get_active_tickets(voyage.voyage_id)) for voyage in
                voyages),
            "total_seats": sum(
                voyage.availability.remaining_seats + voyage.availability.bookings
                for voyage in voyages
                if voyage.availability
            ),
        }
        return summary

    def delete_schedule(self, schedule_id):
        schedule = self.schedule_repo.get(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found.")

        for voyage in schedule.voyages:
            availability = self.availability_repo.get_by_voyage(voyage.voyage_id)
            if availability:
                self.session.delete(availability)

            tickets = self.ticket_repo.get_active_tickets(voyage.voyage_id)
            for ticket in tickets:
                self.session.delete(ticket)

            self.session.delete(voyage)

        self.session.delete(schedule)
        self.session.commit()
        return schedule_id
