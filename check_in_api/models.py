from check_in_api import db

class Attendee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    branch = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    
class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False)
    
class Ticket(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    checked_in = db.Column(db.Boolean(), nullable=False, default=False)
    attendee = db.Column('Attendee',db.ForeignKey('attendee.id'),nullable=False)
    event = db.Column('Event',db.ForeignKey('event.id'),nullable=False)