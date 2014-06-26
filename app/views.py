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
        return render_template('login.html', form=form, now=datetime.now())

@app.route('/delete')
def delete():
    # The way I solved the ability to delete multiple Reservations at a time
    # was to search the table for a Reservation that had the same user and
    # system with an hour added to the datetime.  Continue this search by
    # adding an hour each time until no Reservation is found. This would
    # account for the case where a user would reserve more than one hour
    # at a time.
    #
    # To do this, I had to extract a bunch of data from the first Reservation
    # and then use it to build subsequent queries on the table.
    res_id = request.args.get('res_id')
    reservation = Reservation.query.get(res_id)
    user_id = reservation.reserved_by
    sys = reservation.device
    res_date = reservation.res_datetime
    date_str = res_date.date().isoformat()
 
    # delete first record
    db.session.delete(reservation)
   
    search = True
    while search:
        res_date = res_date + timedelta(hours=1)
        next_res = Reservation.query.filter(Reservation.res_datetime == res_date, Reservation.reserved_by == user_id, Reservation.device == sys).all()
    
        if next_res:
            db.session.delete(next_res[0])
        else:
            search = False
    
    # commit all changes    
    db.session.commit()
    
    # go back to the hours page for the right date
    return redirect(url_for('hours', date_str = date_str))

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
    # determine the date to query; if None use today()
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
    # TODO: make time default to UTC
    hour_list = []
    start_t = datetime.combine(date.today(), time(hour=0))
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
    return render_template('hours.html', date_str=date_str, hour_list=hour_list, systems=systems, matrix=matrix, now=datetime.now())
