from flask import Flask, render_template, flash, redirect, session, url_for, jsonify, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, Form
from wtforms.validators import DataRequired, Length

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


# @app.route('/user', methods=['GET', 'POST'])
# def user():
#     # form = LoginForm()
#     form = {}
#     form['userid'] = request.values.get('userid')
#     form['passwd'] = request.values.get('passwd')
#     form['house'] = request.values.get('house')
#     form['submit'] = request.values.get('submit')
#     if form.get('submit') :
#         return str(form)
#     return 'hello'

# @app.route('/user', methods=['GET', 'POST'])
# def user():
#     form = LoginForm(request.form)
#     print(form.userid.data)
#     if form.validate():
#         return form.userid.data
#     return 'hello'


# @app.route('/user', methods=['GET','POST'])
# def user():
#     form = LoginForm(request.form)
#     if form.validate():
#         userid = form.userid.data
#         passwd = form.passwd.data
#         area = form.area.data
#         house = form.house.data
#         print(userid)
#         print(passwd)
#         global to_Charge
#         global to_View
#         with app.app_context():
#             msg = login_post(userid, passwd, area, house)
#             if msg:
#                 to_Charge = msg[0]
#                 to_View = msg[1]
#             else:
#                 # flash("网络异常, 请尝试重新登陆", 'warning')
#                 return redirect(url_for("index"))
#         return redirect(url_for('money'))
#     return str([userid, passwd, area, house])


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

# @app.route('/user', methods=['GET','POST'])
# def user():
#     form = LoginForm()
#     if form.validate_on_submit():
#         userid = form.userid.data
#         passwd = form.passwd.data
#         area = form.area.data
#         house = form.house.data
#         print(userid)
#         print(passwd)
#         global to_Charge
#         global to_View
#         with app.app_context():
#             msg = login_post(userid, passwd, area, house)
#             if msg:
#                 to_Charge = msg[0]
#                 to_View = msg[1]
#             else:
#                 # flash("网络异常, 请尝试重新登陆", 'warning')
#                 return redirect(url_for("index"))
#         return redirect(url_for('money'))
#     return 'hello'



@app.route('/user', methods=['GET','POST'])
def user():
    form = LoginForm(request.form)
    if form.validate():
        userid = form.userid.data
        passwd = form.passwd.data
        area = form.area.data
        house = form.house.data
        print(userid)
        print(passwd)
        # global to_Charge
        # global to_Views
        # with app.app_context():
            # msg = login_post(userid, passwd, area, house)
        msg = [{'a':'1','b':'2','c':'3'}, {'a':'1','b':'2','c':'3'}]
        # msg = login_post(userid, passwd, area, house)
        if msg:
            current_app.config['to_Charge'] = msg[0]
            current_app.config['to_View'] = msg[1]
        else:
        #     # flash("网络异常, 请尝试重新登陆", 'warning')
            return redirect(url_for("index"))
        # # return redirect(url_for('money'))
        # # print(current_app.config)
        print(type(current_app.config['to_Charge']))
        return jsonify(msg)
    return jsonify({'code':form.errors})



@app.route('/money', methods=['GET','POST'])
def money():
    form = CostForm(request.form)
    if form.validate():
        money = form.money.data
        to_Charge = current_app.config['to_Charge']
        # Charge(to_Charge['s'], to_Charge['userpassword'], to_Charge['MyMoney'], to_Charge['value_1'], to_Charge['value_2'], money)
        print(to_Charge)
        
        return '完事了！'
    return render_template('user.html')
    


# @app.route('/money', methods=['GET','POST'])
# def money():
#     # global to_View
#     # global to_Charge
#     form = CostForm()
#     # now_money = to_View['MyMoney']
#     # now_ele = to_View['surplus_ele']
#     if form.validate_on_submit():
#         money = form.money.data
#         Charge(to_Charge['s'], to_Charge['userpassword'], to_Charge['MyMoney'], to_Charge['value_1'], to_Charge['value_2'], money)
#         flash('成功充值 %s ' % money)
#         # return redirect('done')
#     return render_template('money.html', form=form, now_money=now_money, now_ele=now_ele)
#     # return json.dumps(resu, ensure_ascii=False)
@app.route('/done')
def done():
    return '完事了'



if __name__ == '__main__':
    app.run()