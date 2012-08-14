import datetime
from tornado import web
from pectin.web import MediaApplicationMixin, TemplateApplicationMixin,\
        TemplateMixin, MediaMixin
from pectin.database import SQLAlchemy
from pectin import forms
from tornado import httpserver, ioloop, options
from wtforms import TextField
from sqlalchemy import Column, String

database = SQLAlchemy("sqlite:///test.sqlite")


class BaseHandler(forms.AutoFormsMixin, TemplateMixin, MediaMixin,
        web.RequestHandler):
    pass


class TestForm(forms.Form):
    text = TextField("Text Field")


class Item(database.Model):
    content = Column(String)


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


class DataBaseTestHandler(BaseHandler):
    @property
    def item_list(self):
        return Item.query.all()

    @property
    def Form(self):
        return TestForm

    def get(self):
        self.render("dbtest.html", list=self.item_list)

    def post(self):
        form = self.getform()
        database.session.add(Item(content=form.text.data))
        try:
            database.session.commit()
        except:
            database.create_db()
            database.session.rollback()
            database.session.commit()
        self.render("dbtest.html", list=self.item_list)


class Application(TemplateApplicationMixin, MediaApplicationMixin,
        web.Application):
    def __init__(self):
        handlers = [
            ("/", HelloHandler),
            ("/forms/?", FormsTestHandler),
            ("/dbtest/?", DataBaseTestHandler),
        ]
        super(Application, self).__init__(handlers, debug=True,
                template_path="templates", media_path="media")


options.parse_command_line()
http_server = httpserver.HTTPServer(Application())
http_server.listen(8888)
ioloop.IOLoop.instance().start()  # Start IO Loop.
