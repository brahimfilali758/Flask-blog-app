from flask import Flask, render_template , redirect , url_for , request , flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY']='lkdfjglsdfjgljdlmfkgjdlj565'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique = True , nullable = False )
    email = db.Column(db.String(120) , unique = True , nullable = False )
    password = db.Column(db.String(60) , nullable = False)
    posts = db.relationship('Post' , backref = 'author')

class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(20) , nullable = False )
    content = db.Column(db.String(120) , nullable = False )
    date_posted = db.Column(db.DateTime , )
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html' , title = "Home page")


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




if __name__ == '__main__':
    app.run(debug=True)
