import urllib
from flask_restful import Api
from resources.users import User
from resources.users_admin import UsersAdmin, UserAdmin
from resources.events import Events
from resources.signup import Signup
from resources.login import login_api
from resources.errors import errors


def initialize_routes(app):
    api = Api(app, errors=errors)
    app.register_blueprint(login_api, url_prefix="/auth")
    api.add_resource(Signup, "/auth/signup")
    api.add_resource(User, "/api/user")
    api.add_resource(UsersAdmin, "/api/admin/users")
    api.add_resource(UserAdmin, "/api/admin/users/<string:user_handle>")
    api.add_resource(Events, "/api/events")


def log_routes(app):
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
