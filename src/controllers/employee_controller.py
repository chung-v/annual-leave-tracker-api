from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.employee import Employee, employee_schema, employees_schema
from models.leave_request import LeaveRequest, leave_request_schema
from utils import auth_as_admin_decorator

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

# View approved leave in upcoming month for a specific employee (by name)
@employee_bp.route("/", methods=["GET"])
@jwt_required()
def view_approved_leaves_for_employee_by_name():
    # Get employee first and last name from query parameters
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    
    if not first_name or not last_name:
        return {"error": "Please provide both first name and last name."}, 400
    
    # Get the current date and the date 30 days from now
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    
    # Query the employee by name
    employee = Employee.query.filter_by(first_name=first_name, last_name=last_name).first()
    
    if not employee:
        return {"error": f"Employee with name {first_name} {last_name} not found."}, 404
    
    # Query for approved leave requests for the specified employee within the next 30 days
    approved_leaves = LeaveRequest.query.filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.status == 'approved',
        LeaveRequest.start_date.between(start_date, end_date)
    ).all()
    
    # Return the leave requests as a JSON response
    return leave_request_schema.dump(approved_leaves, many=True, exclude=['id']), 200

# View approved leave in upcoming month for a specific team
@employee_bp.route("/team/<int:team_id>", methods=["GET"])
@jwt_required()
def view_approved_leaves_in_team(team_id):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    
    # Check if the team exists
    employees = Employee.query.filter_by(team_id=team_id).all()
    if not employees:
        return {"error": f"Team ID {team_id} not found."}, 404

    # Loop through the employees and get their approved leave requests
    approved_leaves = []
    
    for employee in employees:
        leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.status == 'approved',
            LeaveRequest.start_date.between(start_date, end_date)
        ).all()
        approved_leaves.extend(leaves)
    
    # Return error if no approved leaves are found for any employees in the team
    if not approved_leaves:
        return {"message": f"No approved leave requests found in the upcoming month for team {team_id}."}, 404

    # Return the list of approved leaves
    return leave_request_schema.dump(approved_leaves, many=True, exclude=['id']), 200

# View approved leave in upcoming month in specific department
@employee_bp.route("/department/<int:department_id>", methods=["GET"])
@jwt_required()
def view_approved_leaves_in_department(department_id):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    
    # Check if the department exists
    employees = Employee.query.filter_by(department_id=department_id).all()
    if not employees:
        return {"error": f"Department ID {department_id} not found."}, 404

    # Loop through the employees and get their approved leave requests
    department_approved_leaves = []

    for employee in employees:
        employee_data = employees_schema.dump(employee)
        leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.status == 'approved',
            LeaveRequest.start_date.between(start_date, end_date)
        ).all()
        employee_data['approved_leaves'] = leave_request_schema.dump(leaves, many=True, exclude=['id'])
        department_approved_leaves.append(employee_data)

    # Return approved leaves or error if no leaves are found
    if not department_approved_leaves:
        return {"message": f"No approved leave requests found for department ID {department_id} in the upcoming month."}, 404
    
    return department_approved_leaves, 200

# View all leaves in a specific month (admin only)
@employee_bp.route("/leaves/<int:year>/<int:month>", methods=["GET"])
@jwt_required()
@auth_as_admin_decorator
def view_all_leaves(year, month):
    # Validate the month and year
    try:
        # Calculate start and end dates for the specified month
        start_date = datetime(year, month, 1)
        if month == 12:  # December
            end_date = datetime(year + 1, 1, 1)  # January of the next year
        else:
            end_date = datetime(year, month + 1, 1)  # First day of the next month

        # Query for leave requests in the specified date range
        leaves = LeaveRequest.query.filter(
            LeaveRequest.start_date >= start_date,
            LeaveRequest.start_date < end_date
        ).all()
        
        return leave_request_schema.dump(leaves, many=True), 200
    except ValueError:
        return {"error": "Invalid month or year provided."}, 400
