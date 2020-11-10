from marshmallow import Schema, fields, validates, ValidationError, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Email())
    first_name = fields.Str(required=True, data_key="firstName")
    last_name = fields.Str(required=True, data_key="lastName")
    password = fields.Str(required=True, load_only=True)

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