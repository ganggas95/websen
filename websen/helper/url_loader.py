from werkzeug.utils import cached_property, import_string
from websen import app


class LazyMapper(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)


def url_mapper(url_rules, import_name, **options):
    view = LazyMapper('websen.' + import_name)
    if type(url_rules) is not list and url_rules.startswith("/"):
        app.add_url_rule(url_rules, view_func=view, **options)
    else:
        for url_rule in url_rules:
            app.add_url_rule(url_rule, view_func=view, **options)

