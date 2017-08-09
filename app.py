# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 15:07
@file: app.py
'''
from __future__ import unicode_literals

from flask_thridy import Thridy
from flask import Flask,request,jsonify


app = Flask(__name__)
app.config['THRIDY_AUTH_TYPE_LIST'] =['SINA','QQ']
app.config['THRIDY_AUTH_SINA_ID'] = '2157431491'
app.config['THRIDY_AUTH_SINA_KEY'] = '636787d305eb0948d279f25161f54777'
app.config['THRIDY_AUTH_SINA_REDIRECT'] = 'http://test.howdata.cn/weibo_login/authorized'

app.config['THRIDY_AUTH_QQ_ID'] = '101369632'
app.config['THRIDY_AUTH_QQ_KEY'] = 'd8f98de5edc72c2cf933aeb442426d7f'
app.config['THRIDY_AUTH_QQ_REDIRECT'] = 'http://test.howdata.cn/auth/qq_login/authorized'

app.config['SECRET_KEY'] = '222aa'
thridy = Thridy()



@app.route('/')
def index():
    return thridy.sina_authorize()

@app.route('/qq')
def qq():
    return thridy.qq_authorize()


@app.route('/weibo_login/authorized')
def weibo_author():
    resp = thridy.sina_authorize_response()
    data = {"access_token": resp['access_token'], "uid": resp['uid']}
    user_data = thridy.sina_get_user(data)
    return jsonify(user_data)

@app.route('/auth/qq_login/authorized')
def qq_author():
    resp = thridy.qq_authorize_response()
    data = {"access_token":resp['access_token']}
    resp = thridy.qq_get_user_info(data)
    return jsonify(resp)



if __name__ == '__main__':
    thridy.init_app(app)
    app.run(port=80,host='0.0.0.0',use_reloader=True,threaded=True)