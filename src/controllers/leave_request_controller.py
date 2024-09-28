from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.leave_request import LeaveRequest, leave_request_schema, leave_requests_schema
from utils import auth_as_admin_decorator

leave_request_bp = Blueprint("leave_request", __name__, url_prefix="/leave_request")

# View all employee's own leave requests
@leave_request_bp.route("/", methods=["GET"])
@jwt_required()
def view_own_leave_requests():
    employee_id = get_jwt_identity()
    leave_requests = LeaveRequest.query.filter_by(employee_id=employee_id).all()
    return leave_requests_schema.dump(leave_requests), 200

# View specific employee's own leave request
@leave_request_bp.route("/<int:leave_request_id>", methods=["GET"])
@jwt_required()
def view_specific_leave_request(leave_request_id):
    employee_id = get_jwt_identity()
    leave_request = LeaveRequest.query.filter_by(id=leave_request_id, employee_id=employee_id).first()
    if leave_request:
        return leave_request_schema.dump(leave_request), 200
    return {"error": "Leave request not found."}, 404

# Add new leave request
@leave_request_bp.route("/", methods=["POST"])
@jwt_required()
def add_leave_request():
    body_data = request.get_json()
    leave_request = LeaveRequest(
        employee_id=get_jwt_identity(),
        start_date=body_data.get("start_date"),
        end_date=body_data.get("end_date"),
        reason=body_data.get("reason"),
        status="pending"
    )
    db.session.add(leave_request)
    db.session.commit()
    return leave_request_schema.dump(leave_request), 201

# Cancel leave request
@leave_request_bp.route("/<int:leave_request_id>", methods=["DELETE"])
@jwt_required()
def cancel_leave_request(leave_request_id):
    employee_id = get_jwt_identity()
    leave_request = LeaveRequest.query.filter_by(id=leave_request_id, employee_id=employee_id).first()
    if leave_request:
        db.session.delete(leave_request)
        db.session.commit()
        return {"message": "Leave request cancelled."}, 200
    return {"error": "Leave request not found."}, 404

# Submit request to edit leave request
@leave_request_bp.route("/<int:leave_request_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_leave_request(leave_request_id):
    body_data = request.get_json()
    employee_id = get_jwt_identity()
    leave_request = LeaveRequest.query.filter_by(id=leave_request_id, employee_id=employee_id).first()
    if leave_request:
        leave_request.start_date = body_data.get("start_date", leave_request.start_date)
        leave_request.end_date = body_data.get("end_date", leave_request.end_date)
        leave_request.reason = body_data.get("reason", leave_request.reason)
        db.session.commit()
        return leave_request_schema.dump(leave_request), 200
    return {"error": "Leave request not found."}, 404

# Approve leave request (admin only)
@leave_request_bp.route("/<int:leave_request_id>/approve", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def approve_leave_request(leave_request_id):
    leave_request = LeaveRequest.query.get(leave_request_id)
    if leave_request:
        leave_request.status = "approved"
        db.session.commit()
        return leave_request_schema.dump(leave_request), 200
    return {"error": "Leave request not found."}, 404
