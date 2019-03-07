from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required
from ..models import Subscribe

class DiseaseForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    symptoms = TextAreaField('Symptoms', validators=[Required()])
    control = StringField('Control', validators=[Required()])
    category = SelectField('Category', choices=[('Fungal plant pathogens', 'Fungal plant pathogens'), 
    ('Wheat diseases', 'Wheat diseases'), 
    ('Cercospora', 'Cercospora'), 
    ('Species of mushrooms', 'Species of mushrooms')], validators=[Required()])
    submit = SubmitField('Submit', validators=[Required()])

# class UpdateProfile(FlaskForm):
#     bio = TextAreaField('Your Bio.',validators = [Required()])
#     submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    names = StringField('Username', validators=[Required()])
    symptoms = TextAreaField('Leave a comment:', validators=[Required()])
    submit = SubmitField('Submit')

class AgronomistForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    title = TextAreaField('Leave a title:', validators=[Required()])
    submit = SubmitField('Submit')

class User_diseasesForm(FlaskForm):
    symptom = StringField('Symptom', validators=[Required()])
    submit = SubmitField('Submit')


# class SubscribeForm(FlaskForm):
#     email = StringField('Email', validators=[Required()])
#     submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField('Email ', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        email = Subscribe.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already subscribed to our emailing list.')
