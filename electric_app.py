from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)

from flask_bootstrap import Bootstrap
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

bootstrap = Bootstrap(app)

class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(1,20)])
    body = TextAreaField('Message', validators=[DataRequired(),Length(1,500)])
    submit = SubmitField()


class LoginForm(FlaskForm):
    xuehao = StringField('学号', validators=[DataRequired(), Length(10,10)])
    passwd = PasswordField('密码', validators=[DataRequired(), Length(1,50)])
    # loucheng = StringField('')
    submit = SubmitField('登陆')

class CostForm(FlaskForm):
    danyuan = StringField('单元号', validators=[DataRequired(), Length(2.5)])
    housenumber = StringField("寝室号", validators=[DataRequired(), Length(2,5)])
    money = StringField("充值", validators=[DataRequired(), Length(1,20)])
    submit = SubmitField("登陆")
@app.route('/')
def index():
    form = LoginForm()
    if form.validate_on_submit():
        xuehao = form.xuehao.data
        passwd = form.passwd.data
        login
    return render_template("electric.html")
if __name__ == '__main__':
    app.run()