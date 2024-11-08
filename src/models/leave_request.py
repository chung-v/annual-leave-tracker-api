from datetime import date
from init import db, ma
from marshmallow import fields, validates_schema, ValidationError

class LeaveRequest(db.Model):
    # Name of the table
    __tablename__ = "leave_request"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    # Relationships
    employee = db.relationship('Employee', back_populates='leave_requests')
    status = db.relationship('Status', back_populates='leave_requests')

    __table_args__ = (
        db.UniqueConstraint('employee_id', 'start_date', 'end_date', name='uix_employee_dates'),
    )

class LeaveRequestSchema(ma.Schema):
    # Nested relationship fields
    employee = fields.Nested('EmployeeSchema', only=["first_name", "last_name"])
    status = fields.Nested('StatusSchema', only=["status_name"])

    # Fields for validation
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    # Date range validation
    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data['start_date'] > data['end_date']:
            raise ValidationError("Start date must be before or the same as the end date.")
        if data['start_date'] < date.today():
            raise ValidationError("Start date cannot be in the past.")

    class Meta:
        # Fields to expose
        fields = ("id", "employee_id", "employee", "start_date", "end_date", "status_id", "status")

# To handle a single leave request object
leave_request_schema = LeaveRequestSchema(exclude=["employee_id", "employee", "status_id"])

# To handle a list of leave request objects
leave_requests_schema = LeaveRequestSchema(many=True, exclude=["employee_id"])