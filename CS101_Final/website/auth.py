from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import *
from logging.config import stopListening
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        netID = request.form.get('netID')
        password = request.form.get('password')

        user = User.query.filter_by(netID=netID).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#jaden's function to get dates for documents:
#date of entry is passed in as a parameter
def return_deadlines(date_of_entry):
    # this will be changed to take from the database
    #print(f"Enter Date/Intended Date of Arrival (YYYY-MM-DD):{date_of_entry}\n\n")
    
#    today = datetime.now()
#   today = today.strftime("%Y-%m-%d")
#    print("Today's Date:", today, "\n")

#    if not 0 < month < 13:
#       print('enter a valid month')
#       raise Exception('month must be 01-12')
#    elif not 0 < day < 32:
#       print('enter a valid date')
#       raise Exception(f'{day} is not a valid date in {month}') 
    year = date_of_entry.year
    month = date_of_entry.month
    day = date_of_entry.day

    # submit health insurance form
    health_insurance = date_of_entry - timedelta(days = 3)
    #health_insurance = datetime.strftime("%Y-%m-%d")

    # calculating the deadline for 24hr Form
    deadline24hr = date_of_entry + timedelta(days = 1)
    #deadline24hr = datetime.strftime("%Y-%m-%d")

    # calulating the deadline for Residence Permit Appointment
    permit_date = datetime(year, month+1, day)
    #permit_date = datetime.strftime("%Y-%m-%d")

    res_permit_deadline = permit_date - timedelta(days = 1)
    #res_permit_deadline = datetime.strftime("%Y-%m-%d")

    # Health Check recommended day 
    health_check_date = date_of_entry + timedelta(days = 6)
    #health_check_date = datetime.strftime("%Y-%m-%d")

    # Health Checkup suggested last day
    health_check_deadline = permit_date - timedelta(days = 7)
    #health_check_deadline = datetime.strftime("%Y-%m-%d")

    # SIM Card suggested timeline
    simdate = date_of_entry + timedelta(days = 2)
    #simdate = datetime.strftime("%Y-%m-%d")

    # Bank Account suggested
    bankdate = date_of_entry + timedelta(days = 3)
    #bankdate = bankdate.strftime("%Y-%m-%d")

    return health_insurance, deadline24hr, permit_date, res_permit_deadline, health_check_date, health_check_deadline, simdate, bankdate


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        netID = request.form.get('netID')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        date_of_entry_str = request.form.get('dateOfEntry')
        date_of_entry = datetime.strptime(date_of_entry_str, '%Y-%m-%d')

        user = User.query.filter_by(netID=netID).first()
        if user:
            flash('A User with this NetID already exists.', category='error')
        elif len(netID) > 6:
            flash('NetID must be no greater than 6 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not (date_of_entry):
            flash('Please enter your date of entry.', category='error')
        else:
            #setting items checked to a list of false values
            itemsChecked = [False, False, False, False, False, False, False, False]
            checkedString = json.dumps(itemsChecked)
            health_insurance, deadline24hr, permit_date, res_permit_deadline, health_check_date, health_check_deadline, simdate, bankdate = return_deadlines(date_of_entry)
            new_user = User(
                netID=netID, 
                first_name=first_name, 
                password=generate_password_hash(password1, method='sha256'),
                arrivaldate=date_of_entry,
                #setting items checked
                #items_checked = checkedString,
                health_insurance = health_insurance, 
                deadline24hr = deadline24hr,
                permit_date = permit_date,
                res_permit_deadline = res_permit_deadline,
                health_check_date = health_check_date,
                health_check_deadline = health_check_deadline,
                simdate = simdate,
                bankdate = bankdate)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)