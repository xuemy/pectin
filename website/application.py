from tornado import web
from pectin.web import MediaApplicationMixin, TemplateApplicationMixin
#from pectin.database import SQLAlchemy
from tornado import httpserver, ioloop, options

#database = SQLAlchemy("sqlite:///test.sqlite")


class HelloHandler(web.RequestHandler):
    def get(self):
        self.write("hello, world")


class Application(TemplateApplicationMixin, MediaApplicationMixin,
        web.Application):
    def __init__(self):
        handlers = [("/", HelloHandler)]
        super(Application, self).__init__(handlers)


options.parse_command_line()
http_server = httpserver.HTTPServer(Application())
http_server.listen(8888)
ioloop.IOLoop.instance().start()  # Start IO Loop.
