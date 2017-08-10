# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 11:38
@file: tecent.py
'''
from __future__ import unicode_literals

import requests
import json

from .error import Thirdy_OAuthException
from flask import request,session
from werkzeug import url_decode


class Tecent:
    '''
     QQ  oauth2接口
    '''

    def __init__(self,QQ_ID,QQ_KEY,QQ_REDIRECT_URL):
        '''
        
        :param QQ_ID:  qq_id
        :param QQ_KEY:   qq_key 
        :param QQ_REDIRECT_URL:    qq 回调地址
        '''
        self._consumer_key = QQ_ID
        self._consumer_secret = QQ_KEY
        self._redirect_url = QQ_REDIRECT_URL
        self._request_token_params ={'scope': 'get_user_info'}
        self._base_url = 'https://graph.qq.com'
        self._authorize_url = '/oauth2.0/authorize'
        self._access_token_url = '/oauth2.0/token'
        self._content_type = 'application/json'
        self._encoding = 'utf-8'

        self.requests = requests.session()

    def authorize(self,state=None,**kwargs):
        '''
          登录的第一步  获取code

        :param state:  state csrf的传参
        :param kwargs: 
        :return: 
        '''
        url = '{0}{1}?response_type=code&client_id={2}&redirect_uri={3}&state={4}'.format(self._base_url,self._authorize_url,
                                                                                          self._consumer_key,self._redirect_url,state
                                                                                          )
        return url

    def authorized_response(self):
        '''
        登录第二步  获取access_token
       :return: 
       '''
        if 'code' in request.args:
            url = self._base_url+self._access_token_url
            data = {
                "grant_type":'authorization_code',
                "client_id": self._consumer_key,
                "client_secret": self._consumer_secret,
                "code": request.args.get ('code'),
                "redirect_uri": self._redirect_url
            }
            resp = self.requests.post(url,(data))
            if resp.status_code not in (200,201):
                raise Thirdy_OAuthException(
                    'Invaild response form Tecent,',
                    type='invaild_response',data=resp.content
                )
            content = self.url_code(resp.content)
            session['tecent_access_token'] = content['access_token']
            return content

    def get_user_open_id(self,access_token):
        '''
         通过access_token 获取open_id
        :param access_token: 
        :return: 
        '''
        open_id_url = self._base_url+'/oauth2.0/me'
        data = {
            'access_token':access_token
        }
        resp = requests.get(open_id_url,data)
        content = self.json_to_dict(resp.content)
        return content

    def get_user_info(self,data):
        '''
       根据access_token 和openid 获取 用户信息
       :param data:  access_token ,openid   <type> dict
       :return: 
       '''
        data = self.get_user_open_id(data['access_token'])
        url = self._base_url+'/user/get_user_info?access_token={0}&oauth_consumer_key={1}&openid={2}&format=json'.format(session['tecent_access_token'],self._consumer_key,
                                                                                                                          data['openid'])
        resp = requests.get(url)
        return json.loads(resp.content)



    def url_code(self,content):
        return url_decode(content,charset=self._encoding).to_dict()

    def json_to_dict(self,x):
        if x.find (b'callback') > -1:
            pos_lb = x.find (b'{')
            pos_rb = x.find (b'}')
            x = x[pos_lb:pos_rb + 1]
        try:
            if type (x) != str:
                x = x.decode ('utf-8')
            return json.loads (x, encoding='utf-8')
        except:
            return x
