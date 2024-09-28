from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.employee import Employee, employees_schema
from models.leave_request import LeaveRequest, leave_request_schema
from models.department import Department, department_schema, departments_schema
from utils import auth_as_admin_decorator

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

department_bp = Blueprint("department", __name__, url_prefix="/department")

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
        return {"message": f"Department ID {department_id}({department.department_name}) deleted successfully."}
    else:
        # return error message
        return {"error": f"Department ID {department_id} not found."}, 404

# Get a list of all employees and their leave requests, sorted by department name (admin only)
@department_bp.route("/list", methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_all_departments():
    stmt = db.select(Department).order_by(Department.department_name.asc())
    departments = db.session.scalars(stmt)
    return departments_schema.dump(departments)





# View approved leave in upcoming month in specific department
# @department_bp.route("/<int:department_id>", methods=["GET"])
# @jwt_required()
# def view_approved_leaves_in_department(department_id):

#     # Query the database for the specific department
#     stmt = db.select(Department).where(Department.id == department_id)
#     department = db.session.scalar(stmt)
    
#     # Check if the department exists
#     if department is None:
#         return {"error": f"Department ID {department_id} not found."}, 404

#     # Serialize the single department object
#     return department_schema.dump(department), 200

    
    # start_date = datetime.today()
    # end_date = start_date + timedelta(days=30)
    
    # # Check if the department exists and fetch employees
    # employees = db.session.execute(
    #     db.select(Employee).filter_by(department_id=department_id)
    # ).scalars().all()

    # if not employees:
    #     return {"error": f"Department ID {department_id} not found."}, 404

    # # Fetch approved leave requests for employees in the department
    # department_approved_leaves = []

    # for employee in employees:
    #     employee_data = employees_schema.dump(employee)

    #     leaves = db.session.execute(
    #         db.select(LeaveRequest).filter(
    #             LeaveRequest.employee_id == employee.id,
    #             LeaveRequest.status == 'approved',
    #             LeaveRequest.start_date.between(start_date, end_date)
    #         )
    #     ).scalars().all()

    #     employee_data['approved_leaves'] = leave_request_schema.dump(leaves, many=True, exclude=['id'])
    #     department_approved_leaves.append(employee_data)

    # # Return approved leaves or error if no leaves are found
    # if not department_approved_leaves:
    #     return {"message": f"No approved leave requests found for department ID {department_id} in the upcoming month."}, 404
    
    # return department_approved_leaves, 200
