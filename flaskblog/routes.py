from PIL import Image
from secrets import token_hex
from os.path import join , splitext
from flaskblog import app , bcrypt , db
from flask import render_template , url_for , flash ,redirect , request
from flaskblog.forms import RegistrationForm , LoginForm , UpdateAccountForm , CreatePostForm
from flaskblog.models import User , Post
from flask_login import login_user , logout_user , current_user , login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
    posts = Post.query.all()
    image_file = url_for('static', filename=join('profile_pics',current_user.image_file))
    return render_template('home.html' , title = "Home page" , posts = posts , image_file = image_file)


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
        return redirect(url_for('account'))
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('update_account.html' , form = form)


def save_picture(form_picture):
    random_hex = token_hex(8)
    _ , f_ext = splitext(form_picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = join(app.root_path , 'static/profile_pics' , picture_file_name)

    output_size = (125 , 125)
    image_scaled = Image.open(form_picture)
    image_scaled.thumbnail(output_size)
    image_scaled.save(picture_path)

    return picture_file_name


@app.route("/create_post" , methods=['GET','POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title = title , content = content , user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published succefully !' , 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html' ,title= 'Create a Post Now !', form = form)

