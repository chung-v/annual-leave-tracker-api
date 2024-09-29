from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.leave_request import LeaveRequest, leave_request_schema, leave_requests_schema
from models.status import Status
from utils import auth_as_admin_decorator

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

leave_request_bp = Blueprint("leave_request", __name__, url_prefix="/leave_request")

# View all leave requests for self
@leave_request_bp.route("", methods=["GET"])
@jwt_required()
def view_leave_requests():
    employee_id = get_jwt_identity()

    # Query leave requests for the current user
    leave_requests = LeaveRequest.query.filter_by(employee_id=employee_id).all()
    
    # If leave requests are found, return them
    if leave_requests:
        return leave_requests_schema.dump(leave_requests), 200
    # Else, return message
    return {"message": "No leave requests found."}, 404

# View specific leave request for self
@leave_request_bp.route("/<int:leave_request_id>", methods=["GET"])
@jwt_required()
def view_specific_leave_request(leave_request_id):
    employee_id = get_jwt_identity()

    # Query specific leave request for the current user
    leave_request = LeaveRequest.query.filter_by(id=leave_request_id, employee_id=employee_id).first()

    # If the leave request is found, return it
    if leave_request:
        return leave_request_schema.dump(leave_request), 200
    # Else, return error message
    return {"error": "Leave request not found."}, 404

# Add new leave request
@leave_request_bp.route("/add", methods=["POST"])
@jwt_required()
def add_leave_request():
    body_data = request.get_json()

    # Validate data before creating the LeaveRequest
    start_date = body_data.get("start_date")
    end_date = body_data.get("end_date")

    # Check if both start_date and end_date are provided
    if not start_date or not end_date:
        return {"error": "Start date and end date are required."}, 400
    # Check if start_date is before the end_date
    if start_date > end_date:
        return {"error": "Start date must be before end date."}, 400

    # Fetch the "pending" status from the database
    pending_status = db.session.query(Status).filter(Status.status_name == "pending").first()
    
    # Create a new leave request model instance
    leave_request = LeaveRequest(
        employee_id=get_jwt_identity(),
        start_date=start_date,
        end_date=end_date,
        status=pending_status  # Set the status to pending
    )

    try:
        db.session.add(leave_request)
        db.session.commit()
        return leave_request_schema.dump(leave_request), 201
    # Error handling
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Leave request with the same dates already exists."}, 400

# Delete leave request
@leave_request_bp.route("/delete/<int:leave_request_id>", methods=["DELETE"])
@jwt_required()
def delete_leave_request(leave_request_id):
    # Fetch the leave request from the database
    stmt = db.select(LeaveRequest).filter_by(id=leave_request_id)
    leave_request = db.session.scalar(stmt)
    
    # If leave request exists, delete the leave request
    if leave_request:
        db.session.delete(leave_request)
        db.session.commit()
        return {"message": f"Leave request ID {leave_request_id} deleted successfully."}, 200
    # Else, return error message
    else:
        return {"error": f"Leave request ID {leave_request_id} not found."}, 404

# Approve leave request (admin only)
@leave_request_bp.route("/approve/<int:leave_request_id>", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def approve_leave_request(leave_request_id):
    # Fetch the leave request from the database
    stmt = db.select(LeaveRequest).filter_by(id=leave_request_id)
    leave_request = db.session.scalar(stmt)
    
    # If leave request exists
    if leave_request:
        # Fetch the "approved" status from the database
        approved_status = db.session.query(Status).filter(Status.status_name == "approved").first()
        # Update the status of the leave request
        leave_request.status = approved_status
        db.session.commit()
        return leave_request_schema.dump(leave_request), 200
    # Else, return error message
    else:
        return {"error": f"Leave request ID {leave_request_id} not found."}, 404
