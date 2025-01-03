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
    def __init__(self, session, voyage_repo, location_repo, ticket_repo, availability_repo):
        super().__init__(session)
        self.voyage_repo = voyage_repo
        self.location_repo = location_repo
        self.ticket_repo = ticket_repo
        self.availability_repo = availability_repo

    def create_voyage_with_schedule(
        self, dep_datetime_utc, arr_datetime_utc, origin_id, destination_id, marketing_number, vehicle_number,
        remaining_seats, bookings, tickets=None
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
        self.session.flush()

        availability = domain.Availability(
            voyage_id=voyage.voyage_id,
            remaining_seats=remaining_seats,
            bookings=bookings,
            is_active=True,
        )
        self.availability_repo.add(availability)

        if tickets:
            for ticket_data in tickets:
                ticket = model.Ticket(
                    ticket_id=None,
                    price=ticket_data["price"],
                    voyage_id=voyage.voyage_id,
                    is_active=ticket_data.get("is_active", True),
                )
                self.ticket_repo.add(ticket)

        self.session.commit()
        return voyage

    def get_schedule(self, start_date=None, end_date=None):
        query = self.session.query(domain.Voyage)
        if start_date:
            query = query.filter(domain.Voyage.dep_datetime_utc >= start_date)
        if end_date:
            query = query.filter(domain.Voyage.dep_datetime_utc <= end_date)
        return query.all()

    def get_full_voyage_details(self, voyage_id):
        voyage = self.voyage_repo.get(voyage_id)
        if not voyage:
            raise ValueError(f"Voyage with ID {voyage_id} not found")

        availability = self.availability_repo.get_by_voyage(voyage_id)
        tickets = self.ticket_repo.get_active_tickets(voyage_id)

        return {
            "voyage": voyage,
            "availability": availability,
            "tickets": tickets,
        }

    def update_voyage_schedule(self, voyage_id, dep_datetime_utc=None, arr_datetime_utc=None):
        voyage = self.voyage_repo.get(voyage_id)
        if not voyage:
            raise ValueError(f"Voyage with ID {voyage_id} not found")

        if dep_datetime_utc:
            voyage.dep_datetime_utc = dep_datetime_utc
        if arr_datetime_utc:
            voyage.arr_datetime_utc = arr_datetime_utc

        self.session.commit()
        return voyage

    def delete_voyage(self, voyage_id):
        voyage = self.voyage_repo.get(voyage_id)
        if not voyage:
            raise ValueError(f"Voyage with ID {voyage_id} not found")

        availability = self.availability_repo.get_by_voyage(voyage_id)
        if availability:
            self.session.delete(availability)

        tickets = self.ticket_repo.get_active_tickets(voyage_id)
        for ticket in tickets:
            self.session.delete(ticket)

        self.session.delete(voyage)
        self.session.commit()
        return voyage_id
