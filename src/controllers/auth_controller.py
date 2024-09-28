from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models import Employee, employee_schema, EmployeeSchema
from utils import auth_as_admin_decorator

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_employee():
    try:
        # Gets the data from the body of the request
        body_data = EmployeeSchema().load(request.get_json())
        
        # Creates an instance of the Employee Model
        employee = Employee(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            team_id=body_data.get("team_id"),
            email=body_data.get("email"),
            is_admin=body_data.get("is_admin", False)  # Defaults to False if not provided
        )
        
        # Hashes the password
        password = body_data.get("password")
        if password:
            employee.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Adds and commits to the DB
        db.session.add(employee)
        db.session.commit()
        # Returns acknowledgement
        return employee_schema.dump(employee), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address is already registered."}, 400

@auth_bp.route("/login", methods=["POST"])
def login_employee():
    # Gets the data from the body of the request
    body_data = request.get_json()
    
    # Finds the employee in DB with that email address
    stmt = db.select(Employee).filter_by(email=body_data.get("email"))
    employee = db.session.scalar(stmt)
    
    # If employee exists and password is correct
    if employee and bcrypt.check_password_hash(employee.password, body_data.get("password")):
        # Create JWT
        token = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=1))
        # Responds back
        return {"email": employee.email, "is_admin": employee.is_admin, "token": token}
    
    else:
        # Responds back with an error message
        return {"error": "Invalid email or password"}, 400

# Updates employee details
@auth_bp.route("/employee/update/", methods=["PUT", "PATCH"])
@jwt_required()
def update_employee():
    # Gets the fields from the body of the request
    body_data = EmployeeSchema().load(request.get_json(), partial=True)
    
    # Fetches the employee from the db
    stmt = db.select(Employee).filter_by(id=get_jwt_identity())
    employee = db.session.scalar(stmt)
    
    # If employee exists
    if employee:
        # Updates the fields as required
        employee.first_name = body_data.get("first_name") or employee.first_name
        employee.last_name = body_data.get("last_name") or employee.last_name
        
        password = body_data.get("password")
        if password:
            employee.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Commits to the DB
        db.session.commit()
        # Returns a response
        return employee_schema.dump(employee)
    
    else:
        # Returns an error response
        return {"error": "Employee does not exist."}, 404

# Updates employee details that only an admin can do
@auth_bp.route("/employee/update/<int:employee_id>", methods=["PUT"])
@jwt_required()
@auth_as_admin_decorator
def update_employee(employee_id):
    # Fetches the employee from the db
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    
    # If employee exists
    if employee:
        # Gets the fields from the body of the request
        body_data = EmployeeSchema().load(request.get_json(), partial=True)
        # Updates the fields as required
        employee.team_id = body_data.get("team_id") or employee.team_id
        # Commits to the DB
        db.session.commit()
        # Returns an acknowledgement message
        return employee_schema.dump(employee)
    
    else:
        # Returns error message
        return {"message": f"Employee with id {employee_id} not found."}, 404

# Deletes employee details that only an admin can do
@auth_bp.route("/employee/delete/<int:employee_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_employee(employee_id):
    # Finds the employee with the id from the db
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    
    # If employee exists
    if employee:
        # Deletes the employee
        db.session.delete(employee)
        db.session.commit()
        # Returns an acknowledgement message
        return {"message": f"Employee with id {employee_id} is deleted."}
    
    else:
        # Returns error message
        return {"message": f"Employee with id {employee_id} not found."}, 404
