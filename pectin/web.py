import tornado
import functools


class Application(tornado.web.Application):
    pass


class RequestHandler(tornado.web.RequestHandler):
    pass


class MediaApplicationMixin(object):
    '''Media File Feature.'''
    def __init__(self, handlers, *args, **settings):
        if self.require_setting("media_path"):
            media_url_prefix = self.settings.get("media_url_prefix", "/media/")
            handlers.append((r"/%s/(.*)" % media_url_prefix, MediaFileHandler))
        super(MediaApplicationMixin, self).__init__(handlers, *args, **settings)


class MediaFileHandler(tornado.web.StaticFileHandler):
    '''
        Media file handler bese on the StaticFileHandler.

            application = web.Application([
                (r"/media/(.*)", pectin.web.MediaFileHandler, {"path": "/var/www"}),
            ])
    '''
    def initialize(self, *args, **kwargs):
        self.require_setting("media_path")
        super(MediaFileHandler, self).initialize(*args, **kwargs)

    @classmethod
    def set_media_settings(cls, settings):
        settings["static_path"] = settings["media_path"]
        settings["static_url_prefix"] = settings.get("media_url_prefix", "/media/")
        return settings

    @property
    def settings(self):
        return self.set_media_settings(self.application.settings)

    @classmethod
    def make_static_url(cls, settings, path):
        settings = cls.set_media_settings(settings)
        super(MediaFileHandler, cls).make_static_url(settings, path)


class MediaMixin(object):
    def media_url(self, path, include_host=None):
        self.require_setting("media_path", "media_url")
        media_handler_class = self.settings.get(
            "media_handler_class", MediaFileHandler)

        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""
        return base + media_handler_class.make_static_url(self.settings, path)


def unauthenticated(method):
    """Decorate methods with this to require that the user be NOT logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
