from flask import Flask, render_template, session, request, redirect, url_for
from forms import NameForm

app = Flask(__name__)
app.secret_key = "gooblegobble"

@app.route('/')
def home():
    if 'name' in session:
        name = session['name']
    else:
        name = None
    return render_template('home.html', name = name)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = NameForm()
    
    if request.method == 'POST':
        session['name'] = form.name.data
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

if __name__ == '__main__':
  app.run(debug=True)