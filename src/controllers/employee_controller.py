from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.employee import Employee, employee_schema
from models.leave_request import LeaveRequest, leave_requests_schema
from models.status import Status

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

# View approved leave in the upcoming month for a specific employee
@employee_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def view_approved_leaves_for_employee(employee_id):
    # Get the current date and the date 30 days from today
    start_date = datetime.today()
    end_date = start_date + timedelta(days=30)

    # Query the employee
    employee = db.session.get(Employee, employee_id)

    if not employee:
        return {"error": f"Employee ID {employee_id} not found."}, 404
    
    # Retrieve the ID for the "approved" status directly from the Status table
    approved_status = db.session.query(Status).filter(Status.status_name == "approved").first()
    
    if not approved_status:
        return {"error": "Approved status not found."}, 404
    
    # Query for approved leave requests for the specified employee within the next 30 days
    leaves_stmt = db.select(LeaveRequest).filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.status_id == approved_status.id,  # Use approved_status.id
        LeaveRequest.start_date.between(start_date, end_date)
    )
    approved_leaves = db.session.execute(leaves_stmt).scalars().all()
    
    return leave_requests_schema.dump(approved_leaves), 200
