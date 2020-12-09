import urllib
from flask_restful import Api
from .users import Users, User
from .events import Events
from .signup import Signup
from .login import login_api
from .errors import errors


def initialize_routes(app):
    api = Api(app, errors=errors)
    app.register_blueprint(login_api, url_prefix="/login")
    api.add_resource(Signup, "/signup")
    api.add_resource(Users, "/api/admin/users")
    api.add_resource(User, "/api/admin/users/<string:user_handle>")
    api.add_resource(Events, "/api/events")
    log_routes(app)


def log_routes(app):
    app.logger.info("Info statement")
    print("-----------------------------------")
    print("ROUTES")
    print("-----------------------------------")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            methods = ",".join(rule.methods)
            route_line = urllib.parse.unquote(
                "{:20s} {:25s} {}".format(rule.endpoint, methods, rule)
            )
            print(route_line)
    print("-----------------------------------")
