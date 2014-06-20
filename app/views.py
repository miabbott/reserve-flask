from datetime import datetime, date, time, timedelta
from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import NameForm
from models import System, Reservation
from app import app, db

@app.before_request
def modify():
  session.modified = True

@app.route('/')
@app.route('/index')
def index():
    if 'name' in session:
        name = session['name']
        return redirect(url_for('hours'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = NameForm()
    
    if request.method == 'POST':
        session['name'] = form.name.data
        return redirect(url_for('hours'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/delete')
def delete():
    res_id = request.args.get('res_id')
    reservation = Reservation.query.get(res_id)
    
    date = reservation.res_datetime.date().isoformat()
    #date_str = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    
    db.session.delete(reservation)
    db.session.commit()
    
    return redirect(url_for('hours', date_str = date))

@app.route('/reserve/')
def reserve():
    # grab the id from the request and query the appropriate System entry
    system_id = request.args.get('system')
    system = System.query.get(system_id)

    # build the datetime for a reservations
    date_list = request.args.get('res_date').split("-")
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    new_date = date(year, month, day)
    
    new_time = time(int(request.args.get('res_time')))
    hours = int(request.args.get('hours'))
    
    new_datetime = datetime.combine(new_date, new_time)

    # get username from session
    reserved_by = session['name']

    # iterate through the hours and create reservations
    for hr in range(hours):
        r = Reservation(res_datetime = new_datetime + timedelta(hours = hr), reserved_by = reserved_by, device = system)
        db.session.add(r)

    # commit all the records
    db.session.commit()
    
    # redirect back to hours page with date specified
    return redirect(url_for('hours', date_str = new_date.isoformat()))

@app.route('/hours/')
@app.route('/hours/<date_str>')
def hours(date_str = None):
    # determine the date to query; if None use today
    if date_str is None:
        date_str = date.today()
    else:
        date_list = date_str.split("-")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        date_str = date(year, month, day)

    # get a list of all the systems in the DB
    systems = System.query.all()
    
    # build a list of 24 hours
    # TODO: make start time configurable
    hour_list = []
    start_t = datetime.combine(date.today(), time(hour=18))
    for hr in range(24):
        new_t = start_t + timedelta(hours=hr)
        hour_list.append(new_t.time())

    # build a dictionary of hours and lists
    # the keys are hours, the value is a zipped list of systems and reservations
    matrix = {}
    for h in hour_list:
        h_row = []
        res_dt = datetime.combine(date_str, h)
        for sys in systems:
            res = sys.is_reserved(res_datetime = res_dt)
            if res is not None:
                h_row.append(res)
            else:
                h_row.append(None)
        zipped = zip(systems, h_row)
        matrix[h] = zipped

    # render the hours template with a date, list of hours, list of systems, and the matrix
    return render_template('hours.html', date_str=date_str, hour_list=hour_list, systems=systems, matrix=matrix)
