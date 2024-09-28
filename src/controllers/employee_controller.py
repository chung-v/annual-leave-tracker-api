from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.employee import Employee, employee_schema
from models.leave_request import LeaveRequest, leave_request_schema

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

# View approved leave in the upcoming month for a specific employee (by name)
@employee_bp.route("/", methods=["GET"])
@jwt_required()
def view_approved_leaves_for_employee_by_name():
    # Get employee first and last name from query parameters
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    
    if not first_name or not last_name:
        return {"error": "Please provide both first name and last name."}, 400
    
    # Get the current date and the date 30 days from today
    start_date = datetime.today()
    end_date = start_date + timedelta(days=30)

    # Query the employee by name
    stmt = db.select(Employee).filter_by(first_name=first_name, last_name=last_name)
    employee = db.session.scalar(stmt)

    if not employee:
        return {"error": f"Employee with name {first_name} {last_name} not found."}, 404
    
    # Query for approved leave requests for the specified employee within the next 30 days
    leaves_stmt = db.select(LeaveRequest).filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.status == 'approved',
        LeaveRequest.start_date.between(start_date, end_date)
    )
    approved_leaves = db.session.execute(leaves_stmt).scalars().all()
    
    # Return the list of approved leaves
    approved_leaves = employee_schema.dump(employee)
    approved_leaves['approved_leaves'] = leave_request_schema.dump(approved_leaves, many=True, exclude=['id'])

    return approved_leaves, 200
