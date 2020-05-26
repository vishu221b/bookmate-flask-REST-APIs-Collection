class ResourceFactory:
    def __init__(self, app, resources):
        self.app = app
        self.resources = resources
        self.resource_blueprints = [x.SingletonResourceFactory()._init_singleton_resource() for x in self.resources]

    def initiate_blueprints(self, app, prints):
        for blueprint in prints:
            app.register_blueprint(blueprint.get('blueprint'))

    def create_blueprints(self):
        self.initiate_blueprints(self.app, self.resource_blueprints)