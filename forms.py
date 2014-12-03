from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, TextAreaField, SubmitField, validators, DateTimeField
from wtforms.validators import required, Length
 
class ContactForm(Form):
  name = TextField("Name",  [validators.Required()])
  email = TextField("Email",  [validators.Required()])
  subject = TextField("Subject",  [validators.Required()])
  message = TextAreaField("Message",  [validators.Required()])
  submit = SubmitField("Send")

class AppointmentForm(Form):
  title = TextField('Title', [Length(max=255)])
  start = DateTimeField('Start', [required()])
  end = DateTimeField('End')
  allday = BooleanField('All Day')
  location = TextField('Location', [Length(max=255)])
  description = TextAreaField('Description')