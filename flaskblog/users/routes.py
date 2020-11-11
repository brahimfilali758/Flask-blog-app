
from os.path import join ,splitext
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users' , __name__)

@users.route("/register" , methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created succefully , Please Login' , 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'Register' , form = form)


@users.route("/login" , methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data) :
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else :
            flash('Please check your email and password !' , 'danger')
    return render_template('login.html', title = 'Login Page' , form = form)


@users.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated :
        logout_user()
        return redirect(url_for('main.home'))
    else :
        return redirect(url_for('users.login'))


@users.route("/account")
@login_required
def account():
    image_file = url_for('static', filename=join('profile_pics',current_user.image_file))
    return render_template('account.html' , title = 'Account' , image_file = image_file)


@users.route("/update_account" , methods=['GET','POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data :
            profile_pic = save_picture(form.picture.data)
            current_user.image_file = profile_pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.new_password.data != '' :
            new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = new_hashed_password
        db.session.commit()
        flash('Your Account has been updated succefully !' , 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('update_account.html' , form = form)


@users.route("/reset_password" , methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to your account with instructions to reset your password' , 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html' , title = 'Reset Password' , form = form)

@users.route("/reset_password/<token>" , methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None :
        flash('That is an invalid or expired token' , 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed succefully , Please Login' , 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html' , title = 'Reset Password' , form = form)
