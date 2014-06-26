from flask_wtf import Form
from wtforms import TextField, SubmitField

class NameForm(Form):
    name = TextField("Please enter a user name:")
    submit = SubmitField("Submit")