from flaskblog import app
from flask import render_template , url_for , flash
from flaskblog.forms import RegistrationForm , LoginForm
from flaskblog.models import User , Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account creted for {form.username.data}' , 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register' , form = form)


@app.route("/login" , methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login Page' , form = form)



