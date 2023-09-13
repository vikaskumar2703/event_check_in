from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from .database import Base


class Attendee(Base):
    __tablename__ = 'attendee'
    attendee_id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    branch = Column(String(), nullable=False)
    year = Column(Integer(), nullable=False)
    attendee_token = Column(String(), nullable=False)


class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    datetime = Column(DateTime(), nullable=False)
    event_token = Column(String(), nullable=False)


class Ticket(Base):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer(), primary_key=True)
    checked_in = Column(Boolean(), nullable=False, default=False)
    attendee_id = Column('Attendee', ForeignKey('attendee.attendee_id'), nullable=False)
    event_id = Column('Event', ForeignKey('event.event_id'), nullable=False)
    ticket_token = Column(String(), nullable=False)
