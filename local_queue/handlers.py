from schedule.domain.commands import (
    CreateLocationCommand,
    UpdateLocationCommand,
    DeleteLocationCommand,
    CreateVoyageCommand,
    UpdateVoyageCommand,
    DeleteVoyageCommand,
    CreateTicketCommand,
    UpdateTicketStatusCommand,
    DeleteTicketCommand,
    SetAvailabilityCommand,
    UpdateAvailabilityCommand,
    CreateScheduleCommand,
    AddVoyageToScheduleCommand,
    DeleteScheduleCommand,
)


class CommandHandler:

    def __init__(self, location_service, voyage_service, ticket_service, availability_service, schedule_service):
        self.location_service = location_service
        self.voyage_service = voyage_service
        self.ticket_service = ticket_service
        self.availability_service = availability_service
        self.schedule_service = schedule_service

    def handle_create_location(self, command: CreateLocationCommand):
        return self.location_service.create_location(
            title=command.title,
            latitude=command.latitude,
            longitude=command.longitude,
        )

    def handle_update_location(self, command: UpdateLocationCommand):
        return self.location_service.update_location(
            location_id=command.location_id,
            title=command.title,
            latitude=command.latitude,
            longitude=command.longitude,
        )

    def handle_delete_location(self, command: DeleteLocationCommand):
        return self.location_service.delete_location(location_id=command.location_id)

    def handle_create_voyage(self, command: CreateVoyageCommand):
        return self.voyage_service.create_voyage(
            dep_datetime_utc=command.dep_datetime_utc,
            arr_datetime_utc=command.arr_datetime_utc,
            origin_id=command.origin_id,
            destination_id=command.destination_id,
            marketing_number=command.marketing_number,
            vehicle_number=command.vehicle_number,
        )

    def handle_update_voyage(self, command: UpdateVoyageCommand):
        return self.voyage_service.update_voyage_schedule(
            voyage_id=command.voyage_id,
            dep_datetime_utc=command.dep_datetime_utc,
            arr_datetime_utc=command.arr_datetime_utc,
        )

    def handle_delete_voyage(self, command: DeleteVoyageCommand):
        return self.voyage_service.delete_voyage(voyage_id=command.voyage_id)

    def handle_create_ticket(self, command: CreateTicketCommand):
        return self.ticket_service.create_ticket(
            voyage_id=command.voyage_id,
            price=command.price,
            is_active=command.is_active,
        )

    def handle_update_ticket_status(self, command: UpdateTicketStatusCommand):
        return self.ticket_service.update_ticket_status(
            ticket_id=command.ticket_id,
            is_active=command.is_active,
        )

    def handle_delete_ticket(self, command: DeleteTicketCommand):
        return self.ticket_service.delete_ticket(ticket_id=command.ticket_id)

    def handle_set_availability(self, command: SetAvailabilityCommand):
        return self.availability_service.set_availability(
            voyage_id=command.voyage_id,
            remaining_seats=command.remaining_seats,
            bookings=command.bookings,
            is_active=command.is_active,
        )

    def handle_update_availability(self, command: UpdateAvailabilityCommand):
        return self.availability_service.update_availability(
            voyage_id=command.voyage_id,
            remaining_seats=command.remaining_seats,
            bookings=command.bookings,
            is_active=command.is_active,
        )

    def handle_create_schedule(self, command: CreateScheduleCommand):
        return self.schedule_service.create_schedule(schedule_date=command.schedule_date)

    def handle_add_voyage_to_schedule(self, command: AddVoyageToScheduleCommand):
        return self.schedule_service.add_voyage_to_schedule(
            schedule_id=command.schedule_id,
            dep_datetime_utc=command.dep_datetime_utc,
            arr_datetime_utc=command.arr_datetime_utc,
            origin_id=command.origin_id,
            destination_id=command.destination_id,
            marketing_number=command.marketing_number,
            vehicle_number=command.vehicle_number,
        )

    def handle_delete_schedule(self, command: DeleteScheduleCommand):
        return self.schedule_service.delete_schedule(schedule_id=command.schedule_id)
