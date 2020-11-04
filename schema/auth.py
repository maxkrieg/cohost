import re
from marshmallow import Schema, fields, validates, ValidationError


class SignupDataSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    first_name = fields.Str(required=True, data_key="firstName")
    last_name = fields.Str(required=True, data_key="lastName")
    password = fields.Str(required=True, load_only=True)

    @validates("email")
    def validate_email(self, email):
        email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        is_valid = re.match(email_regex, email)
        if not is_valid:
            raise ValidationError(field_name="email", message="Bad email format")

    @validates("password")
    def validate_password(self, password):
        error_messages = []
        if len(password) < 6 or len(password) > 18:
            error_messages.append("Password must be between 7 and 18 characters long")

        if not any(char.isdigit() for char in password):
            error_messages.append("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            error_messages.append("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            error_messages.append("Password should have at least one lowercase letter")

        if not any(char in ["$", "@", "#", "%"] for char in password):
            error_messages.append(
                "Password should have at least one of the symbols $@#%"
            )

        if len(error_messages) > 0:
            raise ValidationError(", ".join(error_messages))


class LoginDataSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)