from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json
from datetime import *

views = Blueprint('views', __name__)

#get the deadline function
def getDeadline(dbDate, isChecked=False):
    #subtracting the 0000000
    dbDate= dbDate.replace(" 00:00:00",'')

    if isChecked:
        deadline = "You've already completed this task, good job!"
    elif dbDate:
        deadline_date = datetime.strptime(dbDate, "%Y-%m-%d")
        days_until_deadline = (deadline_date - datetime.now()).days
        if days_until_deadline < 0:
            deadline = "Your deadline has passed, you better get this done!"
        elif days_until_deadline == 0:
            deadline = "Deadline is today!"
        elif days_until_deadline == 1:
            deadline = "Deadline is tommorow!"
        else:
            deadline = f"{days_until_deadline} days until deadline..."
    else:
        deadline = "Deadline not found..."
    
    return deadline


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Retrieve the checklist from the database
    #checklist = json.loads(current_user.items_checked)

    # Map checkbox names to checklist items
    checkbox_map = {
        'healthcare': current_user.insurance_check,
        'arrival': current_user.hasArrived,
        'accomodation': current_user.accomodation_check,
        'phonenumber': current_user.sim_check,
        'bankacc': current_user.bank_check,
        'healthcheckup': current_user.checkup_check,
        'EEB': current_user.eeb_check,
        'ResidencePermit': current_user.permitHasArrived
    }

    #sets username after pulling the first name from the user's database item
    username = current_user.first_name or "Treasured User"

     # Calculates the number of days until the health insurance deadline
    health_insurance = getDeadline(current_user.health_insurance,current_user.insurance_check)

    arrivalDeadline = current_user.arrivaldate
    arrivalDeadline = datetime.combine(arrivalDeadline, time.min)
    if current_user.hasArrived:
        arrivalDate = "How do you like China?"
    elif arrivalDeadline:
        days_until_deadline = (arrivalDeadline - datetime.now()).days
        if days_until_deadline < 0:
            arrivalDate = "Welcome to China!"
        elif days_until_deadline == 0:
            arrivalDate = "Have a safe flight!"
        else:
            arrivalDate = f"{days_until_deadline} days until your arrival!"
    else:
        arrivalDate = "Date not found..."

    twofourHR = getDeadline(current_user.deadline24hr,current_user.accomodation_check)
    phoneNum = getDeadline(current_user.simdate,current_user.sim_check)
    bank = getDeadline(current_user.bankdate,current_user.bank_check)
    checkup = getDeadline(current_user.health_check_deadline,current_user.checkup_check)
    eeb = getDeadline(current_user.permit_date,current_user.eeb_check)


    if request.method == 'POST': 
    # Update checkbox_map with checked checkboxes
        for key in checkbox_map:
            checkbox_value = request.form.get(key)
            checkbox_map[key] = True if checkbox_value == 'on' else False
    
    #if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        #if len(note) < 1:
            #flash('Note is too short!', category='error') 
        #else:
           #new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            #db.session.add(new_note) #adding the note to the database 
            #db.session.commit()
            #('Note added!', category='success')

    return render_template("mainpage.html",checkbox_map=checkbox_map,user=current_user,username=username,insureDL=health_insurance,arrivalDL=arrivalDate,tfhrDL=twofourHR,phoneDL=phoneNum,bankDL=bank,checkDL=checkup,eebDL=eeb)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/insurance', methods=['GET'])
@login_required
def insurance():

    health_insurance=current_user.health_insurance.replace(" 00:00:00","")

    return render_template('insurance.html', user=current_user, healthDL=health_insurance,insCheck=current_user.insurance_check)

@views.route('/accomodation', methods=['GET'])
@login_required
def accomodation():

    twofour = current_user.deadline24hr.replace(" 00:00:00","")

    return render_template('24hr.html', user=current_user,twofourDL=twofour)

@views.route('/arrival', methods=['GET'])
@login_required
def arrival():

    arrivalDay=current_user.arrivaldate

    return render_template('arrival.html', user=current_user, arrivalDL=arrivalDay)

@views.route('/bank', methods=['GET'])
@login_required
def bank():

    bankDate=current_user.bankdate.replace(" 00:00:00","")

    return render_template('bank.html', user=current_user, bankDL=bankDate)

@views.route('/phone', methods=['GET'])
@login_required
def phone():

    simDate=current_user.simdate.replace(" 00:00:00","")

    return render_template('phone.html', user=current_user, phoneDL=simDate)

@views.route('/checkup', methods=['GET'])
@login_required
def checkup():

    checkDate=current_user.health_check_deadline.replace(" 00:00:00","")

    return render_template('checkup.html', user=current_user, checkDL=checkDate)

@views.route('/eeb', methods=['GET'])
@login_required
def eeb():

    eebDate=current_user.permit_date.replace(" 00:00:00","")

    return render_template('eeb.html', user=current_user,eebDL=eebDate)

@views.route('/extra', methods=['GET'])
@login_required
def extra():

    return render_template('extra.html', user=current_user)

@views.route('/update_checklist', methods=['POST'])
@login_required
def update_checklist():
    # get the current user's checklist from the POST request

    current_user.insurance_check = request.json.get('healthcare', False)
    current_user.hasArrived = request.json.get('arrival', False)
    current_user.accomodation_check = request.json.get('accomodation', False)
    current_user.sim_check = request.json.get('phonenumber', False)
    current_user.bank_check = request.json.get('bankacc', False)
    current_user.checkup_check = request.json.get('healthcheckup', False)
    current_user.eeb_check = request.json.get('EEB', False)
    current_user.permitHasArrived = request.json.get('ResidencePermit', False)

    db.session.commit()
    
    #Flash a message to indicate that the changes have been saved
    flash('Your changes have been saved!', category='success')

    return jsonify({'success': True})