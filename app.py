from flask import Flask, render_template , redirect , url_for , request , flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']='lkdfjglsdfjgljdlmfkgjdlj565'

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
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register' , form = form)


@app.route("/login" , methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login Page' , form = form)




if __name__ == '__main__':
    app.run(debug=True)
