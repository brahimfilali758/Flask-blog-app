from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post , User
from flaskblog.posts.forms import CreatePostForm , UpdatePostForm



posts = Blueprint('posts' , __name__)

@posts.route("/create_post" , methods=['GET','POST'])
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
        return redirect(url_for('main.home'))
    return render_template('create_post.html' ,title= 'Create a Post Now !', form = form)


@posts.route("/post/<int:post_id>" , methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html' , title = post.id , post = post)



@posts.route("/post/<int:post_id>/update" , methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdatePostForm()
    if post.author != current_user :
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been Updated succefully ! ' , 'success')
        return redirect(url_for('posts.post' , post_id = post.id))
    elif request.method == 'GET' :
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html' , title = 'Update Post : ' + post.title , form = form)



@posts.route("/my_posts")
@login_required
def my_posts():
    posts = Post.query.filter_by(author = current_user).all()
    return render_template('my_posts.html' , title = 'My Posts' , posts = posts)


@posts.route("/post/<int:post_id>/delete" , methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted succefully ! ' , 'info')
    return redirect(url_for('main.home'))



@posts.route("/user/<string:username>" , methods=['GET','POST'])
def user_posts(username):
    page = request.args.get('page' ,1 ,type=int )
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page = page , per_page = 2 )
    return render_template('user_posts.html' , title = username , posts = posts)
