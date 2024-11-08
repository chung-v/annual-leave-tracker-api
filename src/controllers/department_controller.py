from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.department import Department, department_schema, departments_schema
from utils import auth_as_admin_decorator

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

department_bp = Blueprint("department", __name__, url_prefix="/department")

# View a list of all departments
@department_bp.route("/list", methods=['GET'])
@jwt_required()
def get_all_departments():
    stmt = db.select(Department).order_by(Department.department_name.asc())
    departments = db.session.scalars(stmt)
    return departments_schema.dump(departments), 200

# Create a new department (admin only)
@department_bp.route('/add', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def create_department():
    try:
        # Get data from the body of the request
        department_data = department_schema.load(request.get_json())

        # Create a new department model instance
        department = Department(
            department_name = department_data.get("department_name"),
        )

        # Add and commit to the database
        db.session.add(department)
        db.session.commit()
        # Return acknowledgement
        return department_schema.dump(department), 201

    # Error handling
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"{department.department_name} Department is already registered."}, 400
    
# Delete a department (admin only)
@department_bp.route("/delete/<int:department_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_department(department_id):
    # Fetch the department from the database
    stmt = db.select(Department).filter_by(id=department_id)
    department = db.session.scalar(stmt)

    # If department exists, delete the department
    if department:
        db.session.delete(department)
        db.session.commit()
        return {"message": f"Department ID {department_id} ({department.department_name}) deleted successfully."}, 200
    # Else, return error message
    else:
        return {"error": f"Department ID {department_id} not found."}, 404