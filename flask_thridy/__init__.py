# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 11:38
@file: __init__.py
'''
from __future__ import unicode_literals


from flask import Flask,redirect
from .sina import Sina


__version = '0.0.1'

import os


class Thridy(object):

    def __init__(self,app=None):

        if app:
            self.init_app(app)

    def init_app(self,app):
        if not app or not isinstance (app, Flask):
            raise Exception ('Invalid Flask application instance')

        config = app.config.copy()
        config.setdefault('THRIDY_AUTH_TYPE')
        config.setdefault('THRIDY_AUTH_QQ_ID',None)
        config.setdefault('THRIDY_AUTH_QQ_KEY',None)
        config.setdefault('THRIDY_AUTH_SINA_ID',None)
        config.setdefault('THRIDY_AUTH_SINA_KEY',None)
        config.setdefault('THRIDY_AUTH_WECHAT_ID',None)
        config.setdefault('THRIDY_AUTH_WECHAT_KEY',None)
        config.setdefault('THRIDY_AUTH_WECHAT_REDIRECT',None)

        if not config['THRIDY_AUTH_TYPE']:
            raise Exception('pleace select config "THRIDY_AUTH_TYPE" ')

        if config['THRIDY_AUTH_TYPE'] == 'QQ':
            if not config['THRIDY_AUTH_QQ_ID'] or not config['THRIDY_AUTH_QQ_KEY']:
                raise Exception('Pleace set config "THRIDY_AUTH_QQ_ID" or "THRIDY_AUTH_QQ_KEY" ')

        if config['THRIDY_AUTH_TYPE'] == 'SINA':
            if not config['THRIDY_AUTH_SINA_ID'] or not config['THRIDY_AUTH_SINA_KEY']:
                raise Exception('Pleace set config "THRIDY_AUTH_SINA_ID" or "THRIDY_AUTH_SINA_KEY" ')

            self.sina = Sina(config['THRIDY_AUTH_SINA_ID'],config['THRIDY_AUTH_SINA_KEY'])

        if config['THRIDY_AUTH_TYPE'] == 'WECHAT':
            if not config['THRIDY_AUTH_WECHAT_ID'] or not config['THRIDY_AUTH_WECHAT_KEY'] or not config['THRIDY_AUTH_WECHAT_REDIRECT']:
                raise Exception ('Pleace set config "THRIDY_AUTH_WECHAT_ID" or "THRIDY_AUTH_WECHAT_KEY" or "THRIDY_AUTH_WECHAT_REDIRECT" ')

        if config['THRIDY_AUTH_WECHAT_REDIRECT']:
            if not config['THRIDY_AUTH_WECHAT_REDIRECT'].startswith('http://') or not config['THRIDY_AUTH_WECHAT_REDIRECT'].startswith('https://'):
                raise Exception('Invaild WECHAT_REDIRECT URL')

        if not hasattr(app,'extensions'):
            app.extensions = {}

        app.extensions['thridy_auth'] = self

    def sina_authorize(self,callback=None,state=None,**kwargs):
        url = self.sina.authorize(callback=callback,state=state,**kwargs)
        return redirect(url)

    def sina_authorize_response(self):
        data = self.sina.authorized_response()
        return data

    def sina_get_user(self,url,data):
        data = self.sina.get_user(url,data)
        return data


class Thirdy_OAuthException(RuntimeError):
    def __init__(self, message, type=None, data=None):
        self.message = message
        self.type = type
        self.data = data

