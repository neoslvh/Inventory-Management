from flasgger import Swagger


def register_swagger(app):
    Swagger(app)