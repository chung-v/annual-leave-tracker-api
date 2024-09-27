from flask_jwt_extended import get_jwt_identity

import functools

from init import db
from models.user import User

#  Checks if the current user is an admin before allowing the decorated function to execute.
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Gets the user's id from get_jwt_identity.
        user_id = get_jwt_identity()
        # Fetches the user from the database.
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # If the user is an admin, the function is executed.
        if user.is_admin:
            return fn(*args, **kwargs)
        # If not, error 403 is returned.
        else:
            return {"error": "Only admin can perform this action"}, 403
    
    return wrapper