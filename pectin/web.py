import tornado.web
import functools
from jinja2 import Environment, FileSystemLoader


class Application(tornado.web.Application):
    pass


class RequestHandler(tornado.web.RequestHandler):
    pass


class TemplateApplicationMixin(object):
    def __init__(self, *args, **settings):
        super(TemplateApplicationMixin, self).__init__(*args, **settings)
        if "template_path" not in settings:
            return
        if "template_loader" in settings:
            loader = settings['template_loader']
        else:
            loader = FileSystemLoader(settings['template_path'])
        del self.ui_modules['Template']
        if "debug" in settings:
            auto_reload = settings["debug"]
        else:
            auto_reload = False
        self.template_environment = Environment(
            loader=loader,
            auto_reload=auto_reload,
            autoescape=False,)


class TemplateMixin(object):
    def render_string(self, template_name, **context):
        self.require_setting("template_path", "render")
        default_context = {
            'xsrf': self.xsrf_form_html,
            'request': self.request,
            'settings': self.settings,
            'current_user': self.current_user,
            'static_url': self.static_url,
            'handler': self,
        }
        context.update(default_context)
        context.update(self.ui)  # Enabled tornado UI methods.
        template = self.application.template_environment.get_template(
            template_name)
        return template.render(**context)


class MediaApplicationMixin(object):
    '''Media File Feature, routing files that users upload.'''
    def __init__(self, handlers, *args, **settings):
        if "media_path" in settings:
            handlers.append((r"/media/(.*)", MediaFileHandler,
                             {"path": settings["media_path"]}))
        super(MediaApplicationMixin, self).__init__(
            handlers, *args, **settings)


class MediaFileHandler(tornado.web.StaticFileHandler):
    '''
        Media file handler bese on the StaticFileHandler.

            application = web.Application([
                (r"/media/(.*)", pectin.web.MediaFileHandler,
                 {"path": "/var/www"}),
            ])
    '''
    def initialize(self, *args, **kwargs):
        self.require_setting("media_path")
        super(MediaFileHandler, self).initialize(*args, **kwargs)

    @classmethod
    def set_media_settings(cls, settings):
        settings["static_path"] = settings["media_path"]
        settings["static_url_prefix"] = settings.get(
            "media_url_prefix", "/media/")
        return settings

    @property
    def settings(self):
        return self.set_media_settings(self.application.settings)

    @classmethod
    def make_static_url(cls, settings, path):
        settings = cls.set_media_settings(settings)
        return tornado.web.StaticFileHandler.make_static_url(settings, path)


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

    def render_string(self, template_name, **context):
        if hasattr(self, "media_url"):
            context["media_url"] = self.media_url
        super(MediaMixin, self).render_string(template_name, **context)


def unauthenticated(method):
    """Decorate methods with this to require that the user be NOT logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


__all__ = ["Application", "RequestHandler", "TemplateApplicationMixin",
           "TemplateMixin", "MediaApplicationMixin", "MediaMixin",
           "MediaFileHandler", "unauthenticated"]
