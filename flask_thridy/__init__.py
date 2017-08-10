# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 11:38
@file: __init__.py
'''
from __future__ import unicode_literals

from flask import Flask, redirect, request
from .sina import Sina
from .tecent import Tecent
from .wechat import Wechat
from .error import Thirdy_OAuthException

import re
import os

__version__ = '0.0.1'


class Thridy(object):
    def __init__(self, app=None):

        if app:
            self.init_app(app)

    def init_app(self, app):
        if not app or not isinstance(app, Flask):
            raise Exception('Invalid Flask application instance')

        config = app.config.copy()
        config.setdefault('THRIDY_AUTH_TYPE')
        config.setdefault('THRIDY_AUTH_TYPE_LIST',[])
        config.setdefault('THRIDY_AUTH_QQ_ID', None)
        config.setdefault('THRIDY_AUTH_QQ_KEY', None)
        config.setdefault('THRIDY_AUTH_QQ_REDIRECT', None)
        config.setdefault('THRIDY_AUTH_SINA_ID', None)
        config.setdefault('THRIDY_AUTH_SINA_KEY', None)
        config.setdefault('THRIDY_AUTH_SINA_REDIRECT', None)
        config.setdefault('THRIDY_AUTH_WECHAT_ID', None)
        config.setdefault('THRIDY_AUTH_WECHAT_KEY', None)
        config.setdefault('THRIDY_AUTH_WECHAT_REDIRECT', None)

        if not config['THRIDY_AUTH_TYPE'] and not config['THRIDY_AUTH_TYPE_LIST']:
            raise Exception('pleace select config "THRIDY_AUTH_TYPE" ')

        if not isinstance(config['THRIDY_AUTH_TYPE_LIST'],list):
            raise Thirdy_OAuthException('Pleace set config  AUTH_TYPE_LIST type list ')

        if config['THRIDY_AUTH_TYPE'] == 'QQ' or 'QQ' in config['THRIDY_AUTH_TYPE_LIST']:
            if not config['THRIDY_AUTH_QQ_ID'] or not config['THRIDY_AUTH_QQ_KEY'] or not config[
                'THRIDY_AUTH_QQ_REDIRECT']:
                raise Exception(
                    'Pleace set config "THRIDY_AUTH_QQ_ID" or "THRIDY_AUTH_QQ_KEY" or "THRIDY_AUTH_QQ_REDIRECT"')
            try:
                self.qq = Tecent(config['THRIDY_AUTH_QQ_ID'],config['THRIDY_AUTH_QQ_KEY'],
                                 config['THRIDY_AUTH_QQ_REDIRECT'])
            except:
                raise Thirdy_OAuthException('Params not set , pleacse set Tecent params !')
        else:
            raise Thirdy_OAuthException('Please set THRIDY_AUTH_TYPE  ! ')

        if config['THRIDY_AUTH_TYPE'] == 'SINA' or 'SINA' in config['THRIDY_AUTH_TYPE_LIST']:
            if not config['THRIDY_AUTH_SINA_ID'] or not config['THRIDY_AUTH_SINA_KEY'] or not config[
                'THRIDY_AUTH_SINA_REDIRECT']:
                raise Exception(
                    'Pleace set config "THRIDY_AUTH_SINA_ID" or "THRIDY_AUTH_SINA_KEY" or "THRIDY_AUTH_SINA_REDIRECT" ')
            try:
                self.sina = Sina(config['THRIDY_AUTH_SINA_ID'], config['THRIDY_AUTH_SINA_KEY'],
                                  config['THRIDY_AUTH_SINA_REDIRECT'])
            except:
                raise Thirdy_OAuthException('Params not set ,Please set Sina params !')
        else:
            raise Thirdy_OAuthException('Please set THRIDY_AUTH_TYPE  ! ')

        if config['THRIDY_AUTH_TYPE'] == 'WECHAT' or 'WECHAT' in config['THRIDY_AUTH_TYPE_LIST']:
            if not config['THRIDY_AUTH_WECHAT_ID'] or not config['THRIDY_AUTH_WECHAT_KEY'] or not config[
                'THRIDY_AUTH_WECHAT_REDIRECT']:
                raise Exception(
                    'Pleace set config "THRIDY_AUTH_WECHAT_ID" or "THRIDY_AUTH_WECHAT_KEY" or "THRIDY_AUTH_WECHAT_REDIRECT" ')

            try:
                self.wechat = Wechat(config['THRIDY_AUTH_WECHAT_ID'], config['THRIDY_AUTH_WECHAT_KEY'],
                                  config['THRIDY_AUTH_WECHAT_REDIRECT'])
            except:
                raise Thirdy_OAuthException('Params not set ,Please set Sina params !')
        else:
            raise Thirdy_OAuthException('Please set THRIDY_AUTH_TYPE  ! ')


        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['thridy_auth'] = self

    def sina_authorize(self, state=None, **kwargs):
        '''
          登录的第一步  获取code
         
        :param state:  state csrf的传参
        :param kwargs: 
        :return: 
        '''
        url = self.sina.authorize(state=state, **kwargs)
        return redirect(url)

    def sina_authorize_response(self):
        '''
           登录第二步  获取access_token
        :return: 
        '''
        try :
            data = self.sina.authorized_response()
            return data
        except Exception as e:
            raise Thirdy_OAuthException('Reuqests faild ,Please try again requests  CODE ! ')

    def sina_get_user_info(self, data):
        '''
            根据access_token 和uid 获取 用户信息
        :param data:  access_token ,uid   <type> dict
        :return: 
        '''
        if not data or not isinstance(data, dict):
            raise Thirdy_OAuthException('Reuqest not data or is not dict type ')

        if data.get('access_token') is None:
            raise Thirdy_OAuthException('Please set params Access_token !')
        if data.get('uid') is None:
            raise Thirdy_OAuthException('Please set params uid')

        user_url = 'users/show.json'
        data = self.sina.get_user(user_url, data)
        return data

    def qq_authorize(self,state=None,**kwargs):
        url = self.qq.authorize(state=state,**kwargs)
        return redirect(url)

    def qq_authorize_response(self):
        try:
            data = self.qq.authorized_response()
            return data
        except Exception as e:
            raise Thirdy_OAuthException('Reuqests faild ,Please try again requests  CODE !')

    def qq_get_open_id(self,access_token):
        return self.qq.get_user_open_id(access_token)

    def qq_get_user_info(self,data):
        if not data or not isinstance (data, dict):
            raise Thirdy_OAuthException ('Reuqest not data or is not dict type ')

        if data.get('access_token') is None:
            raise Thirdy_OAuthException ('Please set params Access_token !')

        return self.qq.get_user_info(data)

    def wechat_authorize(self,state=None,**kwargs):
        url = self.wechat.authorize(state=state,**kwargs)
        return redirect(url)

    def wechat_authorize_response(self):
        try:
            data = self.wechat.authorize_response()
            return data
        except Exception as e:
            raise Thirdy_OAuthException('Reuqests faild ,Please try again requests  CODE !')

    def wechat_get_user_info(self,data):
        if not data or not isinstance (data, dict):
            raise Thirdy_OAuthException ('Reuqest not data or is not dict type ')

        if data.get('access_token') is None:
            raise Thirdy_OAuthException ('Please set params Access_token !')

        if data.get('openid') is None:
            raise Thirdy_OAuthException ('Please set params openid !')

        return self.wechat.get_user_info(data)