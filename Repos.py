from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, obj):
        """Добавить объект в хранилище"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Получить объект по идентификатору"""
        pass

    @abstractmethod
    def list(self):
        """Получить все объекты"""
        pass


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def add(self, obj):
        self.session.add(obj)

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def list(self):
        return self.session.query(self.model).all()


class LocationRepository(SQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, model.Location)


class VoyageRepository(SQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, model.Voyage)

    def get_by_origin(self, origin_id):
        return self.session.query(self.model).filter_by(origin_id=origin_id).all()


class TicketRepository(SQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, model.Ticket)

    def get_active_tickets(self, voyage_id):
        return self.session.query(self.model).filter_by(voyage_id=voyage_id, is_active=True).all()


class AvailabilityRepository(SQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, model.Availability)

    def get_by_voyage(self, voyage_id):
        return self.session.query(self.model).filter_by(voyage_id=voyage_id).first()
