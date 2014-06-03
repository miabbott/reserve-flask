from flask_wtf import Form
from wtforms import TextField, SubmitField

class NameForm(Form):
    name = TextField("Name")
    submit = SubmitField("Submit")