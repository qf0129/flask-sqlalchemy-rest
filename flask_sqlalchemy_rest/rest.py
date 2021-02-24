from flask import Blueprint
from .model import RestModel


class Rest(object):

    def __init__(self, app=None, db=None, url_prefix='/api', auth_decorator=None):
        self.app = app
        self.db = db
        self.url_prefix = url_prefix
        self.auth_decorator = auth_decorator
        if app is not None and db is not None:
            self.init_app(app, db, url_prefix, auth_decorator)

    def init_app(self, app, db=None, url_prefix=None, auth_decorator=None):
        self.app = app
        self.db = db or self.db
        self.url_prefix = url_prefix or self.url_prefix
        self.auth_decorator = auth_decorator or self.auth_decorator

    def add_model(self, model, url_name=None, methods=['GET', 'POST', 'PUT', 'DELETE'], ignore_columns=[]):
        model_name = model.__tablename__
        blueprint = Blueprint(f'rest_{model_name}', __name__, url_prefix=self.url_prefix)
        view_func = RestModel.as_view(model_name, db=self.db, model=model, ignore_columns=ignore_columns)
        if self.auth_decorator:
            view_func = self.auth_decorator(view_func)
        url_name = url_name if url_name else model_name

        blueprint.add_url_rule(view_func=view_func, rule=f'/{url_name}', methods=list(set(methods).intersection(set(['GET', 'POST']))))
        blueprint.add_url_rule(view_func=view_func, rule=f'/{url_name}/<int:id>', methods=list(set(methods).intersection(set(['GET', 'PUT', 'DELETE']))))
        if self.app:
            self.app.register_blueprint(blueprint)