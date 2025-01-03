from abc import ABC, abstractmethod

from schedule.adapters import Repos


class AbstractUnitOfWork(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


from sqlalchemy.orm import Session

class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        """
        :param session_factory: callable, создающий экземпляр SQLAlchemy Session
        """
        self.session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def voyages(self):
        return Repos.VoyageRepository(self.session)

    @property
    def locations(self):
        return Repos.LocationRepository(self.session)

    @property
    def tickets(self):
        return Repos.TicketRepository(self.session)

    @property
    def availability(self):
        return Repos.AvailabilityRepository(self.session)
