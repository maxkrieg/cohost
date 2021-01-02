import urllib
from flask_restful import Api
from .users import User
from .users_admin import UsersAdmin, UserAdmin
from .events import Events
from .signup import Signup
from .login import login_api
from .errors import errors


def initialize_routes(app):
    api = Api(app, errors=errors)
    app.register_blueprint(login_api, url_prefix="/auth")
    api.add_resource(Signup, "/auth/signup")
    api.add_resource(User, "/api/user")
    api.add_resource(UsersAdmin, "/api/admin/users")
    api.add_resource(UserAdmin, "/api/admin/users/<string:user_handle>")
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
