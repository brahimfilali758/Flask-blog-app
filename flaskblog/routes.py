from os.path import join
from flaskblog import app , bcrypt , db
from flask import render_template , url_for , flash ,redirect , request
from flaskblog.forms import RegistrationForm , LoginForm , UpdateAccountForm
from flaskblog.models import User , Post
from flask_login import login_user , logout_user , current_user , login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html' , title = "Home page" , posts = posts )


@app.route("/about")
def about():
    return render_template('about.html', title = 'About page')


@app.route("/register" , methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created succefully , Please Login' , 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register' , form = form)


@app.route("/login" , methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data) :
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash('Please check your email and password !' , 'danger')
    return render_template('login.html', title = 'Login Page' , form = form)


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated :
        logout_user()
        return redirect(url_for('home'))
    else :
        return redirect(url_for('login'))


@app.route("/account" )
@login_required
def account():
    image_file = url_for('static', filename=join('profile_pics',current_user.image_file))
    return render_template('account.html' , title = 'Account' , image_file = image_file)



@app.route("/update_account" , methods=['GET','POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        current_user.password = new_hashed_password
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('update_account.html' , form = form)
