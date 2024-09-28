from flask_jwt_extended import get_jwt_identity

from init import db
from models.employee import Employee

import functools


#  Checks if the current employee is an admin before allowing the decorated function to execute.
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Gets the employee's id from get_jwt_identity.
        employee_id = get_jwt_identity()
        # Fetches the employee from the database.
        stmt = db.select(Employee).filter_by(id=employee_id)
        employee = db.session.scalar(stmt)
        # If the employee is an admin, the function is executed.
        if employee.is_admin:
            return fn(*args, **kwargs)
        # If not, error 403 is returned.
        else:
            return {"error": "Only an admin can perform this action."}, 403
    
    return wrapper