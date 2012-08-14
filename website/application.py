from tornado import web
from pectin.web import MediaApplicationMixin, TemplateApplicationMixin,\
        TemplateMixin, MediaMixin
#from pectin.database import SQLAlchemy
from pectin import forms
from tornado import httpserver, ioloop, options
from wtforms import TextField

#database = SQLAlchemy("sqlite:///test.sqlite")


class BaseHandler(forms.AutoFormsMixin, TemplateMixin, MediaMixin,
        web.RequestHandler):
    pass


class TestForm(forms.Form):
    text = TextField("Text Field")


class HelloHandler(BaseHandler):
    def get(self):
        self.render("home.html")


class FormsTestHandler(BaseHandler):
    @property
    def Form(self):
        return TestForm

    def get(self):
        self.render("forms.html")

    def post(self):
        form = self.getform()
        self.render("forms.html", result=form.text.data)


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
