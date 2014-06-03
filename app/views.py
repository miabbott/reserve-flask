from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import NameForm
from app import app, db

@app.before_request
def modify():
  session.modified = True

@app.route('/')
@app.route('/index')
def index():
    if 'name' in session:
        name = session['name']
        return render_template('index.html', name = name)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = NameForm()
    
    if request.method == 'POST':
        session['name'] = form.name.data
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)
