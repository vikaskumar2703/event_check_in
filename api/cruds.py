from sqlalchemy.orm import Session
from secrets import token_hex
from . import models, schemas


def get_attendee(db: Session, attendee_id: int):
    return db.query(models.Attendee).get(attendee_id)


def get_attendee_by_name(db: Session, name: str):
    return db.query(models.Attendee).filter(models.Attendee.name==name).first()


def get_attendee_by_token(db: Session, token: str):
    return db.query(models.Attendee).filter(models.Attendee.attendee_token==token).first()


def get_attendees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendee).offset(skip).limit(limit).all()


def create_attendee(db: Session, attendee: schemas.AttendeeCreate):
    token = token_hex(3)
    db_attendee = models.Attendee(name=attendee.name, branch=attendee.branch, year=attendee.year,attendee_token=token)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee