# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2017-08-08 17:06
@file: setup.py
'''
from __future__ import unicode_literals

from setuptools import setup,find_packages


setup(
    name='Flask-thridy',
    version='0.0.3',
    description='simple use thridy for login you web',
    license='BSD',
    author='Feeeenng',
    author_email='z332007851@163.com',
    url='https://github.com/Feeeenng/flask-thridy',
    platforms = 'any',
    packages = find_packages(),
    zip_safe=False,
    install_requires = [
        'Flask>=0.8',
        'requests>=2.18.3',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]

)