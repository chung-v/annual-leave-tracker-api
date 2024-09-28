from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Length

class Employee(db.Model):
    # Name of the table
    __tablename__ = "employee"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    team = db.relationship('Team', back_populates='employees')
    leave_requests = db.relationship('LeaveRequest', back_populates='employee')

class EmployeeSchema(ma.Schema):
    # Nested fields
    leave_requests = fields.List(fields.Nested('LeaveRequestSchema', exclude=["employee"]))
    team = fields.Nested('TeamSchema', exclude=["employees"])

    # Email format validation
    email = fields.String(required=True, validate=Regexp(r"^\S+@\S+\.\S+$", error="Invalid email format."))

    # Password length validation
    password = fields.String(load_only=True, required=True, validate=Length(min=6, error="Password must be at least 6 characters long."))

    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password", "team_id", "is_admin", "leave_requests", "team")

# To handle a single employee object
employee_schema = EmployeeSchema(exclude=["password"])

# To handle a list of employee objects
employees_schema = EmployeeSchema(many=True, exclude=["password"])
