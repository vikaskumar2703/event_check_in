from fastapi import FastAPI, Depends, HTTPException, requests
from sqlalchemy.orm import Session

from . import models, schemas, cruds
from .database import SessionLocal, engine

from .utils import check_valid

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
     "http://localhost:5173/",
     "http://192.168.1.36:5173/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/attendees/", response_model=schemas.Attendee, tags=['attendees'])
def create_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    if not check_valid(attendee.email):
        raise HTTPException(status_code=400, detail="Email not valid")
    db_attendee = cruds.get_attendee_by_email(db, email=attendee.email)
    if db_attendee:
        raise HTTPException(status_code=400, detail="Email already registered")
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

# qr_str = attendee_token+event_token+ticket_token
@app.post('/check_in/', tags=['check-in'])
def check_in(qr_str: str, db: Session = Depends(get_db)):
    attendee_token = qr_str[:6]
    event_token = qr_str[6:12]
    ticket_token = qr_str[12:]
    db_attendee = cruds.get_attendee_by_token(db=db, token=attendee_token)
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    db_event = cruds.get_event_by_token(db=db, token=event_token)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_ticket = cruds.get_ticket_by_token(db=db, token=ticket_token)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db_ticket = cruds.check_in_ticket(db=db, ticket_token=ticket_token, attendee_token=attendee_token, event_token=event_token)
    if db_ticket is None:
        raise HTTPException(status_code=400, detail="Ticket invalid")
    return {'attendee':{'attendee_id':db_attendee.attendee_id,'name':db_attendee.name,'branch':db_attendee.branch,'year':db_attendee.year},
            'event':{'attendee_id':db_event.event_id,'name':db_event.name},
            'ticket':{'ticket_id':db_ticket.ticket_id,'checked_in':db_ticket.checked_in}}


@app.get('/qr_str/', tags=['misc'])
def get_qr_str(ticket_token: str, db: Session = Depends(get_db)):
    qr_str = cruds.get_qr_str(db=db, ticket_token=ticket_token)
    return {'qr_str':qr_str}
    

## Todo
# @app.post('/revert_check_in/', tags=['check-in'])
# def revert_check_in(qr_str: str, db: Session = Depends(get_db)):
    