# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-08 10:42
@file: error.py
'''
from __future__ import unicode_literals




class Thirdy_OAuthException(RuntimeError):
    def __init__(self, message, type=None, data=None):
        self.message = message
        self.type = type
        self.data = data