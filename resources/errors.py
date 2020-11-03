from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


errors = {
    "InternalServerError": {"message": "Something went wrong", "status": 500},
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401,
        "error": "UnauthorizedError",
    },
    "ValidationError": {"message": "Invalid data provided", "status": 400},
}
