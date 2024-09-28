from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.department import Department, department_schema, departments_schema
from utils import auth_as_admin_decorator

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

department_bp = Blueprint("department", __name__, url_prefix="/department")

# Get a list of all departments
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
        # get the data from the body of the request
        department_data = department_schema.load(request.get_json())
        # create a new department model instance
        department = Department(
            department_name = department_data.get("department_name"),
        )
        # add and commit to the DB
        db.session.add(department)
        db.session.commit()
        # response message
        return department_schema.dump(department), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Department is already registered."}, 400
    
# Delete a department (admin only)
@department_bp.route("/delete/<int:department_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_department(department_id):
    # fetch the department from the database
    stmt = db.select(Department).filter_by(id=department_id)
    department = db.session.scalar(stmt)
    # if department exists
    if department:
        # delete the department
        db.session.delete(department)
        db.session.commit()
        return {"message": f"Department ID {department_id} ({department.department_name}) deleted successfully."}
    else:
        # return error message
        return {"error": f"Department ID {department_id} not found."}, 404