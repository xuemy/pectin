
![Logo](http://github.com/tioover/Pectin/raw/master/example/media/logo.png)

Python web application thin glue layer with [Tornado](http://github.com/facebook/tornado).

## Preparation ##

First, you need to install: 

* Tornado - Web Framework and Server.
* WTForms - Forms verification.
* Jinja2 - HTML Template engine.

Pectin is Loosely coupled. You can choose what components you want to use.
For example, if you do want not use Jinja2, you can remove `TemplateMixin`
from `BaseHandle` or modify `TemplateMixin` to change Template engine.

## Run Example ##
    $ cd example
    $ python2 application.py # or python3.

Then, browser open [0.0.0.0:8888](http://0.0.0.0:8888/)

## Install ##
    $ ./setpy.py # need sudo.

------

Distribution on **MIT LECENSE** .

Overridden form the [Hanger](http://github.com/tioover/hanger) project.
