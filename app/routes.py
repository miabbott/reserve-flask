from flask import Flask, render_template, session, request, redirect, url_for
from forms import NameForm

app = Flask(__name__)
app.secret_key = "gooblegobble"

@app.before_request
def func():
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

if __name__ == '__main__':
  app.run(debug=True)