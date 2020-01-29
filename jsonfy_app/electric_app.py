from flask import Flask, render_template, flash, redirect, session, url_for, jsonify, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, Form
from wtforms.validators import DataRequired, Length

import requests

import os
import json

from login import login_post, Charge
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

from flask_bootstrap import Bootstrap
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

bootstrap = Bootstrap(app)

class LoginForm(Form):
    userid = StringField('学号', validators=[DataRequired(), Length(10,10)])
    passwd = PasswordField('密码', validators=[DataRequired(), Length(1,50)])
    # loucheng = StringField('')
    area = StringField('单元号', validators=[DataRequired(), Length(1.5)])
    house = StringField("寝室号", validators=[DataRequired(), Length(2, 5)])
    submit = SubmitField('登陆')

class CostForm(Form):
    money = StringField("充值", validators=[DataRequired(), Length(1,20)])
    submit = SubmitField("冲！")

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET','POST'])
def user():
    form = LoginForm(request.form)
    if form.validate():
        # userid = form.userid.data
        # passwd = form.passwd.data
        # area = form.area.data
        # house = form.house.data
        current_app.config['userid'] = form.userid.data
        current_app.config['passwd'] = form.passwd.data
        current_app.config['area'] = form.area.data
        current_app.config['house'] = form.house.data
        msg = [{'a':'1','b':'2','c':'3'}, {'a':'1','b':'2','c':'3'}]
       
        # msg = login_post(userid, passwd, area, house)
        # msg = login_post(current_app.config['userid'], current_app.config['passwd'], current_app.config['passwd'], current_app.config['area'], current_app.config['house'])
        if msg:
            current_app.config['to_Charge'] = msg[0]
            current_app.config['to_View'] = msg[1]
        else:
        #     # flash("网络异常, 请尝试重新登陆", 'warning')
            return redirect(url_for("index"))
    return render_template('user.html')



@app.route('/money', methods=['GET', 'POST'])
def money():
    return jsonify({'a':current_app.config['to_Charge']['a'], 'b':current_app.config['to_Charge']['b']})


@app.route('/done', methods=['GET', 'POST'])
def done():
    form_cost = CostForm(request.form)
    if form_cost.validate():
        money = form_cost.money.data
        to_Charge = current_app.config['to_Charge']
        print(money)
        try:
            # Charge(to_Charge['s'], to_Charge['userpassword'], to_Charge['MyMoney'], to_Charge['value_1'], to_Charge['value_2'], money)
            return  money + '完事了' 
        except:
            return "something wrong, please try again."
    return 'error'

if __name__ == '__main__':
    app.run()