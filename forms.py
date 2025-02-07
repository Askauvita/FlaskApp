from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import InputRequired

class NetForm(FlaskForm):
    upload = FileField('Load image', validators=[InputRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    border_size = IntegerField('Border size', validators=[InputRequired()])
    submit = SubmitField('Add border')