from pydantic import BaseModel
from datetime import datetime


class AttendeeBase(BaseModel):
    name: str
    branch: str
    year: int
    email: str


class AttendeeCreate(AttendeeBase):
    pass


class Attendee(AttendeeBase):
    attendee_id: int
    attendee_token: str

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str
    datetime: datetime


class EventCreate(EventBase):
    pass


class Event(EventBase):
    event_id: int
    event_token: str

    class Config:
        orm_mode = True


class TicketBase(BaseModel):
    attendee_id: int
    event_id: int


class TicketCreate(TicketBase):
    pass



class Ticket(TicketBase):
    ticket_id: int
    checked_in: bool
    ticket_token: str

    class Config:
        orm_mode = True
