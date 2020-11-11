from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class CreatePostForm(FlaskForm):
    title = StringField('Title of your post : ' , validators=[DataRequired()])
    content = TextAreaField('Express yourselef :',
                        validators=[DataRequired()] , render_kw={"rows": 10, "cols": 11})

    submit = SubmitField('Submit Your Post')


class UpdatePostForm(FlaskForm):
    title = StringField('Title of your post : ' , validators=[DataRequired()])
    content = TextAreaField('Express yourselef :',
                        validators=[DataRequired()] , render_kw={"rows": 10, "cols": 11})

    submit = SubmitField('Submit Your Post')
