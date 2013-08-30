![Logo](http://github.com/tioover/Pectin/raw/master/example/media/logo.png)

Python web application thin glue layer with [Tornado](http://github.com/facebook/tornado). (chinese: [简单说明](http://eggfan.org/2349))

## Feature ##

* `static` with `media` separate, `media` is the file ueser upload.
* Use Jinja2 template render, not tornado default.
* Integrate WTForms forms framework, had HTML5 forms field support.

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

## Use ##
Place `pectin` folder on your project.

------

Distribution on **MIT LECENSE** .

Overridden form the [Hanger](http://github.com/tioover/hanger) project.
