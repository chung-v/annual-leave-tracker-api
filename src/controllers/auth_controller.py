from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from init import bcrypt, db
from models.employee import Employee, employee_schema, EmployeeSchema
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
@auth_bp.route("/employee/update", methods=["PUT", "PATCH"])
@jwt_required()
def update_employee():
    # Gets the fields from the body of the request
    body_data = EmployeeSchema().load(request.get_json(), partial=True)
    
    # Define allowed fields
    allowed_fields = {"first_name", "last_name", "password"}

    # Check if there are any disallowed fields in the request
    if not all(field in allowed_fields for field in body_data.keys()):
        return jsonify({"error": "You can only update your first name, last name, or password."}), 400

    # Fetches the employee from the db
    stmt = db.select(Employee).filter_by(id=get_jwt_identity())
    employee = db.session.scalar(stmt)
    
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
    

# Updates employee details (admin only)
@auth_bp.route("/employee/update/<int:employee_id>", methods=["PUT", "PATCH"])
@jwt_required()
@auth_as_admin_decorator
def admin_update_employee(employee_id):
    # Fetches the employee from the db
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    
    # If employee exists
    if employee:
        # Gets the fields from the body of the request
        body_data = request.get_json()

        # Define allowed fields for the admin
        admin_allowed_fields = {"first_name", "last_name", "email", "team_id"}

        # Check if there are any disallowed fields in the request
        if not all(field in admin_allowed_fields for field in body_data.keys()):
            return jsonify({"error": "You can only update the employee's first name, last name, email, or team ID."}), 400

        # Load data with schema after validating the fields
        valid_data = EmployeeSchema().load(body_data, partial=True)

        # Updates the fields as required
        employee.first_name = valid_data.get("first_name") or employee.first_name
        employee.last_name = valid_data.get("last_name") or employee.last_name
        employee.email = valid_data.get("email") or employee.email
        employee.team_id = valid_data.get("team_id") or employee.team_id
        
        # Commits to the DB
        db.session.commit()

        # Returns an acknowledgement message
        return employee_schema.dump(employee)
    
    else:
        # Returns error message
        return {"message": f"Employee ID {employee_id} not found."}, 404

# Deletes employee details (admin only)
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
        return {"message": f"Employee ID {employee_id} ({employee.first_name} {employee.last_name}) is deleted."}
    
    else:
        # Returns error message
        return {"message": f"Employee ID {employee_id} not found."}, 404

# Add employee as admin
@auth_bp.route("/employee/admin/<int:employee_id>", methods=["POST"])
@jwt_required()
@auth_as_admin_decorator
def add_admin(employee_id):
    # Find the employee in the database
    employee = Employee.query.get(employee_id)
    if employee:
        # Check if the employee is already an admin
        if employee.is_admin:
            return {"error": f"Employee ID {employee_id} is already an admin."}, 400

        # Add the employee as an admin
        employee.is_admin = True
        db.session.commit()
        return {"message": f"Employee ID {employee_id} is now an admin."}, 200
    return {"error": f"Employee ID {employee_id} not found."}, 404

# Remove employee as admin
@auth_bp.route("/employee/admin/<int:employee_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def remove_admin(employee_id):
    # Find the employee in the database
    employee = Employee.query.get(employee_id)
    if employee:
         # Check if the employee is already not an admin
        if not employee.is_admin:
            return {"error": f"Employee ID {employee_id} is not an admin."}, 400

        # Remove the employee as an admin
        employee.is_admin = False
        db.session.commit()
        return {"message": f"Employee ID {employee_id} is no longer an admin."}, 200
    return {"error": f"Employee ID {employee_id} not found."}, 404