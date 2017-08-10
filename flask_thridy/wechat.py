# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-07 11:39
@file: weixin.py
'''
from __future__ import unicode_literals

import requests
import json

from .error import Thirdy_OAuthException
from flask import request,session


class Wechat:
    '''
     微信oauth2 接口
    '''

    def __init__(self,WECHAT_ID,WECHAT_KEY,WECHAT_REDIRECT_URL):
        '''
        
        :param WECHAT_ID:   微信id
        :param WECHAT_KEY:    微信key
        :param WECHAT_REDIRECT_URL:    微信回调地址 
        '''
        self._consumer_key = WECHAT_ID
        self._consumer_secret = WECHAT_KEY
        self._redirect_url = WECHAT_REDIRECT_URL
        self._request_token_params = {'scope': 'get_user_info'}
        self._base_url = 'https://open.weixin.qq.com'
        self.authorize_url = "https://open.weixin.qq.com/connect/qrconnect"
        self.access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        self.refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"

        self.request = requests.session()

    def authorize(self,state=None,**kwargs):
        '''
          登录的第一步  获取code
         
        :param state:  state csrf的传参
        :param kwargs: 
        :return: 
        '''
        url = '{0}?appid={1}&redirect_uri={2}&response_type=code&scope=snsapi_login&state={3}#wechat_redirect'.format(self.authorize_url,self._consumer_key,
                                                                                                                      self._redirect_url,state
                                                                                                                      )
        return url

    def authorize_response(self):
        '''
           登录第二步  获取access_token
        :return: 
        '''
        if 'code' in request.args:
            url = '{0}?appid={1}&secret={2}&code={3}&grant_type=authorization_code'.format(self.access_token_url,self._consumer_key,
                                                                                           self._consumer_secret,request.args.get('code')
                                                                                           )
            resp = self.request.get(url)
            content = json.loads(resp.content)
            if 'errcode' in content:
                raise Thirdy_OAuthException (
                    'Invaild response form Tecent,',
                    type='invaild_response', data=content
                )
            session['wechat_access_token'] = content['access_token']
            return content

    def get_user_info(self,data):
        '''
        根据access_token 和openid 获取 用户信息
        :param data:  access_token ,openid   <type> dict
        :return: 
        '''
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'.format(data['access_token'],data['openid'])
        resp = self.request.get(url)
        content = json.loads(resp.content)
        if 'errcode' in content:
            raise Thirdy_OAuthException (
                'Invaild response form Tecent,',
                type='invaild_response', data=content
            )
        return content