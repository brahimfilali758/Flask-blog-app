import os
from secrets import token_hex
from PIL import Image
from flask import url_for , current_app
from flask_mail import Message
from flaskblog import  mail
from os.path import splitext , join


def save_picture(form_picture):
    random_hex = token_hex(8)
    _ , f_ext = splitext(form_picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = join(current_app.root_path , 'static/profile_pics' , picture_file_name)

    output_size = (125 , 125)
    image_scaled = Image.open(form_picture)
    image_scaled.thumbnail(output_size)
    image_scaled.save(picture_path)

    return picture_file_name


def send_reset_email(user) :
    token = user.get_reset_token()''
    msg = Message(subject = 'Password Reset Request' , sender = current_app.config.get("MAIL_USERNAME") , recipients = [user.email])

    msg.body = f""" To reset your password , visit the following link :
    {url_for('users.reset_token' , token = token , _external = True)}

    If you did not make this request , then simply ignore this email.
    """

    mail.send(msg)
