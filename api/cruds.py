from sqlalchemy.orm import Session
from secrets import token_hex
from . import models, schemas


def get_attendee(db: Session, attendee_id: int):
    return db.query(models.Attendee).get(attendee_id)


def get_attendee_by_name(db: Session, name: str):
    return db.query(models.Attendee).filter(models.Attendee.name==name).first()


def get_attendee_by_email(db: Session, email: str):
    return db.query(models.Attendee).filter(models.Attendee.email==email).first()


def get_attendee_by_token(db: Session, token: str):
    return db.query(models.Attendee).filter(models.Attendee.attendee_token==token).first()


def get_attendees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendee).offset(skip).limit(limit).all()


def create_attendee(db: Session, attendee: schemas.AttendeeCreate):
    token = token_hex(3)
    db_attendee = models.Attendee(name=attendee.name, email=attendee.email, branch=attendee.branch, year=attendee.year,attendee_token=token)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee


def get_event(db: Session, event_id: int):
    return db.query(models.Event).get(event_id)


def get_event_by_name(db: Session, name: str):
    return db.query(models.Event).filter(models.Event.name==name).first()


def get_event_by_token(db: Session, token: str):
    return db.query(models.Event).filter(models.Event.event_token==token).first()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    token = token_hex(3)
    db_event = models.Event(name=event.name, datetime=event.datetime, event_token=token)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).get(ticket_id)


def get_ticket_by_token(db: Session, token: str):
    return db.query(models.Ticket).filter(models.Ticket.ticket_token==token).first()


def get_tickets_by_attendee(db: Session, attendee_id: int):
    return db.query(models.Ticket).filter(models.Ticket.attendee_id==attendee_id).all()


def get_tickets_by_event(db: Session, event_id: int):
    return db.query(models.Ticket).filter(models.Ticket.event_id==event_id).all()


def check_ticket_exist(db: Session, attendee_id: int, event_id: int):
    return db.query(models.Ticket).filter(models.Ticket.attendee_id==attendee_id).filter(models.Ticket.event_id==event_id).first()


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def check_in_ticket(db: Session, ticket_token: str, attendee_token: str, event_token: str):
    db_ticket = get_ticket_by_token(db=db, token=ticket_token)
    db_attendee = get_attendee(db=db, attendee_id=db_ticket.attendee_id)
    db_event = get_event(db=db, event_id=db_ticket.event_id)
    if db_attendee.attendee_token == attendee_token and db_event.event_token == event_token:
        db_ticket.checked_in = True
        db.commit()
        db.refresh(db_ticket)
        return db_ticket


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    token = token_hex(3)  
    db_ticket = models.Ticket(attendee_id=ticket.attendee_id, event_id=ticket.event_id, ticket_token=token)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
