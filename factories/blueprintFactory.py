from flask import Blueprint
from flask_restful import Api


class BlueprintFactory:
    def __init__(self):
        self.blueprint = None
        self.api = None
        self.generate_fresh_blueprint = lambda x, y: self.create_blueprint(x, y)

    def create_blueprint(self, view, views_path):
        self.blueprint = Blueprint(name=view, import_name=views_path, url_prefix='/{}'.format(str(view)))
        self.api = Api(self.blueprint)
        print(view, views_path)
        return {
            'blueprint': self.blueprint,
            'api': self.api,
            'view': view
        }
