from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    netID = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    arrivaldate = db.Column(db.Date, nullable=False, default=date.today)
    #items_checked = db.Column(db.String(150))

    #variables for the assignment dates
    health_insurance = db.Column(db.String(150))
    deadline24hr = db.Column(db.String(150))
    permit_date = db.Column(db.String(150))
    res_permit_deadline = db.Column(db.String(150))
    health_check_date = db.Column(db.String(150))
    health_check_deadline = db.Column(db.String(150))
    simdate = db.Column(db.String(150))
    bankdate = db.Column(db.String(150))

    #true false for checklist
    insurance_check = db.Column(db.Boolean, default=False)
    hasArrived = db.Column(db.Boolean, default=False)
    accomodation_check = db.Column(db.Boolean, default=False)
    sim_check = db.Column(db.Boolean, default=False)
    bank_check = db.Column(db.Boolean, default=False)
    checkup_check = db.Column(db.Boolean, default=False)
    eeb_check = db.Column(db.Boolean, default=False)
    permitHasArrived = db.Column(db.Boolean, default=False)
    
    notes = db.relationship('Note')