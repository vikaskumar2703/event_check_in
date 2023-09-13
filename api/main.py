from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas, cruds
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/attendees/", response_model=schemas.Attendee, tags=['attendees'])
def create_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    db_attendee = cruds.get_attendee_by_name(db, name=attendee.name)
    if db_attendee:
        raise HTTPException(status_code=400, detail="User already registered")
    return cruds.create_attendee(db=db, attendee=attendee)


@app.get('/attendees/{attendee_id}', response_model=schemas.Attendee, tags=['attendees'])
def get_attendee(attendee_id: int = None, db: Session = Depends(get_db)):
    db_attendee = cruds.get_attendee(db=db, attendee_id=attendee_id)
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return db_attendee


@app.get('/attendees/', response_model=list[schemas.Attendee], tags=['attendees'])
def get_attendees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendees = cruds.get_attendees(db=db, skip=skip, limit=limit)
    return attendees


@app.post("/events/", response_model=schemas.Event, tags=['events'])
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = cruds.get_event_by_name(db, name=event.name)
    if db_event:
        raise HTTPException(status_code=400, detail="Event already exists")
    return cruds.create_event(db=db, event=event)


@app.get('/events/{event_id}', response_model=schemas.Event, tags=['events'])
def get_event(event_id: int = None, db: Session = Depends(get_db)):
    db_event = cruds.get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.get('/events/', response_model=list[schemas.Event], tags=['events'])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = cruds.get_events(db=db, skip=skip, limit=limit)
    return events


@app.post("/tickets/", response_model=schemas.Ticket, tags=['tickets'])
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_attendee = cruds.get_attendee(db=db, attendee_id=ticket.attendee_id)
    if db_attendee is None:
        raise HTTPException(status_code=400, detail="Attendee does not exist")
    db_event = cruds.get_event(db=db, event_id=ticket.event_id)
    if db_event is None:
        raise HTTPException(status_code=400, detail="Event does not exist")
    db_ticket = cruds.check_ticket_exist(
        db=db, attendee_id=ticket.attendee_id, event_id=ticket.event_id)
    if db_ticket:
        raise HTTPException(status_code=400, detail="Ticket already exists.")
    return cruds.create_ticket(db=db, ticket=ticket)


@app.get('/tickets/{ticket_id}', response_model=schemas.Ticket, tags=['tickets'])
def get_ticket(ticket_id: int = None, db: Session = Depends(get_db)):
    db_ticket = cruds.get_ticket(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@app.get('/tickets/', response_model=list[schemas.Ticket], tags=['tickets'])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = cruds.get_tickets(db=db, skip=skip, limit=limit)
    return tickets


@app.get('/check_in/', response_model=schemas.Ticket, tags=['check-in'])
def get_attendee(attendee_token: str, event_token: str, ticket_token: str, db: Session = Depends(get_db)):
    db_ticket = cruds.get_ticket_by_token(db=db, token=ticket_token)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db_ticket = cruds.check_in_ticket(db=db, ticket_token=ticket_token, attendee_token=attendee_token, event_token=event_token)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket invalid")
    return db_ticket