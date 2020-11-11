from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


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
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password')])

    picture = FileField('Update profile picture : ', validators=[FileAllowed(['jpg' , 'png' , 'jpeg'])])

    submit = SubmitField('Update')

    def validate_username(self , username) :
        if username.data != current_user.username :
            user = User.query.filter_by(username=username.data).first()
            if user :
                raise ValidationError('Username is already taken , PLease choose another one !')

    def validate_email(self , email) :
        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError('Email is already taken , PLease choose another one !')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if user is None :
            raise ValidationError('If an account with this email address exists, a password reset message will be sent shortly.')
class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
