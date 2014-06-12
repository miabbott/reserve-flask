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

@app.route('/reserve/')
def reserve():
    system_id = request.args.get('system')
    system = System.query.get(system_id)
    start_time = time(int(request.args.get('start_time')))
    hours = request.args.get('hours')
    
    start_date = date.today()
    end_date = date.today()
    end_time = (datetime.combine(start_date, start_time) + timedelta(hours=int(hours))).time()
    reserved_by = session['name']
    
    r = Reservation(start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, reserved_by=reserved_by, device=system)
    db.session.add(r)
    db.session.commit()
    
    return redirect(url_for('hours'))

#@app.route('/reserve/<date>')
#def reserve(date = date.today()):
#    systems = System.query.all()
#    #hours = [time(i).strftime('%I %p') for i in range(24)]
#    return render_template('reserve.html',
#                           date=date,
#                           systems=systems)

@app.route('/hours/')
@app.route('/hours/<date_str>')
def hours(date_str = None):
    if date_str is None:
        date_str = date.today()
    else:
        date_list = date_str.split("-")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        date_str = date(year, month, day)

    systems = System.query.all()
    hour_list = []
    start_t = datetime.combine(date.today(), time(hour=18))
    for hr in range(24):
        new_t = start_t + timedelta(hours=hr)
        hour_list.append(new_t.time())
        
    matrix = {}
    for h in hour_list:
        h_row = []
        for sys in systems:
            res = sys.is_reserved(date=date_str, time=h)
            if res is not None:
                h_row.append(res)
            else:
                h_row.append(None)
        zipped = zip(systems, h_row)
        matrix[h] = zipped

    return render_template('hours.html', hour_list=hour_list, systems=systems, matrix=matrix)
