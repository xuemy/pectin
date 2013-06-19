from tornado import web
from pectin.web import MediaApplicationMixin, TemplateApplicationMixin,\
        TemplateMixin, MediaMixin
from pectin import forms
from tornado import httpserver, ioloop, options
from wtforms import TextField
from wtforms.validators import Required, Length


class BaseHandler(forms.AutoFormsMixin, TemplateMixin, MediaMixin,
        web.RequestHandler):
    pass


class TestForm(forms.Form):
    text = TextField("Text Field", [Required(), Length(min=2)])


class TestForm2(TestForm):
    pass


class HelloHandler(BaseHandler):
    @web.addslash
    def get(self):
        self.render("home.html")


class FormsTestHandler(BaseHandler):
    @property
    def Form(self):
        return TestForm

    @property
    def formset(self):
        '''Multi-form'''
        return [TestForm2, ]

    @web.addslash
    def get(self):
        self.render("forms.html")

    def post(self):
        try:
            form = self.getform()
        except forms.ValidationError:
            self.render("forms.html")
        else:
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
