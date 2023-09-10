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
def get_attendees(skip: int, limit: int = 100, db: Session = Depends(get_db)):
    attendees = cruds.get_attendees(db=db, skip=skip, limit=limit)
    return attendees


@app.get('/check_in/', response_model=schemas.Ticket, tags=['check-in'])
def get_attendee(attendee_token: str, event_token: str, ticket_token: str, db: Session = Depends(get_db)):
    db_attendee = cruds.get_attendee_by_token(db=db, token=attendee_token)
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")

    # todo: search event and then compare the resulting ticket with the api query ticket
    return {'Not': 'Completed'}
