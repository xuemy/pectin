#!/usr/bin/env python2.7
# coding=utf-8
'''
A framework for simpliy web application programming, base on tornado.
'''
from setuptools import setup

setup(
    name='Pectin',
    version='0.9',
    url='http://github.com/tioover/Pectin/',
    license='MIT',
    author='tioover',
    author_email='tioover@gmail.com',
    description='Pectin web glue layer.',
    long_description=__doc__,
    packages=['pectin', 'pectin.forms'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Tornado',
        'Jinja2',
        'WTForms',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
