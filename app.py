# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 15:07
@file: app.py
'''
from __future__ import unicode_literals

from flask_thridy import Thridy
from flask import Flask,url_for,request,jsonify


app = Flask(__name__)
app.config['THRIDY_AUTH_TYPE_LIST'] =['SINA']
app.config['THRIDY_AUTH_SINA_ID'] = ''
app.config['THRIDY_AUTH_SINA_KEY'] = ''
app.config['THRIDY_AUTH_SINA_REDIRECT'] = ''
app.config['SECRET_KEY'] = '222aa'
thridy = Thridy()



@app.route('/')
def index():
    return thridy.sina_authorize()


@app.route('/weibo_login/authorized')
def weibo_author():
    resp = thridy.sina_authorize_response()
    data = {"access_token": resp['access_token'], "uid": resp['uid']}
    user_data = thridy.sina_get_user(data)
    return jsonify(user_data)



if __name__ == '__main__':
    thridy.init_app(app)
    app.run(port=80,host='0.0.0.0',use_reloader=True,threaded=True)