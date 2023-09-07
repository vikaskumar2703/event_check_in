from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Model


class Attendee(Model):
    attendee_id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    branch = Column(String(), nullable=False)
    year = Column(Integer(), nullable=False)


class Event(Model):
    event_id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    datetime = Column(DateTime(), nullable=False)


class Ticket(Model):
    ticket_id = Column(Integer(), primary_key=True)
    checked_in = Column(Boolean(), nullable=False, default=False)
    attendee = Column('Attendee', ForeignKey('attendee.id'), nullable=False)
    event = Column('Event', ForeignKey('event.id'), nullable=False)
