from flask import Flask, render_template, flash, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
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

class LoginForm(FlaskForm):
    userid = StringField('学号', validators=[DataRequired(), Length(10,10)])
    passwd = PasswordField('密码', validators=[DataRequired(), Length(1,50)])
    # loucheng = StringField('')
    area = StringField('单元号', validators=[DataRequired(), Length(1.5)])
    house = StringField("寝室号", validators=[DataRequired(), Length(2, 5)])
    submit = SubmitField('登陆')

class CostForm(FlaskForm):
    money = StringField("充值", validators=[DataRequired(), Length(1,20)])
    submit = SubmitField("冲！")

to_View = {}
to_Charge= {}


@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        userid = form.userid.data
        passwd = form.passwd.data
        area = form.area.data
        house = form.house.data
        global to_Charge
        global to_View
        with app.app_context():
            msg = login_post(userid, passwd, area, house)
            if msg:
                to_Charge = msg[0]
                to_View = msg[1]
            else:
                flash("网络异常, 请尝试重新登陆", 'warning')
                return redirect(url_for("index"))
        return redirect(url_for('money'))
    return render_template("electric_app.html", form=form)


@app.route('/money', methods=['GET','POST'])
def money():
    global to_View
    global to_Charge
    form = CostForm()
    now_money = to_View['MyMoney']
    now_ele = to_View['surplus_ele']
    if form.validate_on_submit():
        money = form.money.data
        Charge(to_Charge['s'], to_Charge['userpassword'], to_Charge['MyMoney'], to_Charge['value_1'], to_Charge['value_2'], money)
        flash('成功充值 %s ' % money)
        # return redirect('done')
    return render_template('money.html', form=form, now_money=now_money, now_ele=now_ele)
    # return json.dumps(resu, ensure_ascii=False)
@app.route('/done')
def done():
    return '完事了'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=12345)
