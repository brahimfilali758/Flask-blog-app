from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from flaskblog.models import User , Post


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self , username) :
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username is already taken , PLease choose another one !')

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('Email is already taken , PLease choose another one !')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired() ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update')

    def validate_username(self , username) :
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username is already taken , PLease choose another one !')

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('Email is already taken , PLease choose another one !')
