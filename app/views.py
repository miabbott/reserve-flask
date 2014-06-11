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
        return redirect(url_for('reserve'))
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

#@app.route('/reserve')
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
        
    matrix = []
    for h in hour_list:
        h_row = [h.strftime("%H:%M %p")]
        for sys in systems:
            res = sys.is_reserved(date=date_str, time=h)
            if res is not None:
                h_row.append(res)
            else:
                h_row.append(None)
        h_row.append(h.strftime("%H:%M %p"))
        matrix.append(h_row)

    return render_template('hours.html', hour_list=hour_list, systems=systems, matrix=matrix)
