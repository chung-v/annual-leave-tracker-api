from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# Define valid statuses for leave requests
VALID_STATUSES = (
    "pending",    # When the employee submits a leave request and is waiting for approval
    "approved",   # When the leave request is approved by admin
    "cancelled",  # When the employee cancels their leave request
)

class Status(db.Model):
    # Name of the table
    __tablename__ = "status"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationships
    leave_requests = db.relationship('LeaveRequest', back_populates='status')


class StatusSchema(ma.Schema):
    # Nested relationship field
    leave_requests = fields.List(fields.Nested('LeaveRequestSchema', exclude=["status"]))

    # Validate status name against predefined values
    status_name = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        # Fields to expose
        fields = ("id", "status_name", "leave_requests")


# To handle a single status object
status_schema = StatusSchema()

# To handle a list of status objects
statuses_schema = StatusSchema(many=True)
