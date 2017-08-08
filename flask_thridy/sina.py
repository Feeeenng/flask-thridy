# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 11:38
@file: weibo.py
'''
from __future__ import unicode_literals

import requests
import json

from .error import Thirdy_OAuthException
from flask import request,session,redirect,url_for

class Sina:

    def __init__(self,SINA_ID,SINA_KEY,SINA_URL):
        self._consumer_key = SINA_ID
        self._consumer_secret = SINA_KEY
        self._redirect_url = SINA_URL
        self._request_token_params = {'scope': 'email'}
        self._base_url = 'https://api.weibo.com/2/'
        self._authorize_url = 'https://api.weibo.com/oauth2/authorize'
        self._request_token_url = None
        self._request_token_params = None
        self._request_token_method = None
        self._access_token_params = None,
        self._access_token_method = 'POST'
        self._access_token_url = 'https://api.weibo.com/oauth2/access_token'
        self._access_token_headers = None or {}
        self._content_type = 'application/json'
        self._tokengetter = None
        self._encoding = 'utf-8'
        self.app_key = None

        self.requests = requests.session()

    def authorize(self,state=None,**kwargs):
        url = '{0}?client_id={1}&response_type=code&redirect_uri={2}'.format(self._authorize_url,self._consumer_key,self._redirect_url)
        session['oauth_callback'] = self._redirect_url
        return url

    def authorized_response(self):
        if 'code' in request.args:
            url = self._access_token_url
            data = {
                "client_id":self._consumer_key,
                "client_secret":self._consumer_secret,
                "grant_type":'authorization_code',
                "code":request.args.get('code'),
                "redirect_uri":session['oauth_callback']
            }
            resp = self.requests.post(url,data)
            content = json.loads(resp.content)
            if 'error_code' in content:
                if content['error_code'] == 21325:
                     raise Thirdy_OAuthException('Code hasn been Expired, Pleace again code !')
                else:
                    raise content
            else:
                return content
        else:
            raise Thirdy_OAuthException('The reuqests not code ')


    def get_user(self,url,data):
        resp = requests.get(self._base_url+url,data)
        return json.loads(resp.content)
