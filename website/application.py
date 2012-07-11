from tornado import web
from pectin.web import MediaApplicationMixin, TemplateApplicationMixin
#from pectin.database import SQLAlchemy
from pectin import forms
from tornado import httpserver, ioloop, options
from wtforms import TextField

#database = SQLAlchemy("sqlite:///test.sqlite")


class TestForm(forms.Form):
    text = TextField("Text Field")


class HelloHandler(web.RequestHandler):
    def get(self):
        self.render("home.html")


class FormsTestHandler(web.RequestHandler):
    Form = TestForm

    def get(self):
        self.render("forms.html")


class Application(TemplateApplicationMixin, MediaApplicationMixin,
        web.Application):
    def __init__(self):
        handlers = [
            ("/", HelloHandler),
            ("/forms/?", FormsTestHandler),
        ]
        super(Application, self).__init__(handlers, debug=True,
                template_path="templates", media_path="media")


options.parse_command_line()
http_server = httpserver.HTTPServer(Application())
http_server.listen(8888)
ioloop.IOLoop.instance().start()  # Start IO Loop.
