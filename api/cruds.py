from sqlalchemy.orm import Session

from . import models, schemas


def get_attendee(db: Session, attendee_id: int):
    return db.query(models.Attendee).get(attendee_id)

def get_attendees(db: Session, skip: int = 0, limit: int=100):
    return db.query(models.Attendee).offset(skip).limit(limit).all()


