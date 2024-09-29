from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

class Status(db.Model):
    # Name of the table
    __tablename__ = "status"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String, nullable=False, unique=True)

    # Relationships
    leave_requests = db.relationship('LeaveRequest', back_populates='status')

class StatusSchema(ma.Schema):
    # Nested relationship field
    leave_requests = fields.List(fields.Nested('LeaveRequestSchema', exclude=["status"]))

    # Validate status name against predefined values using the database records
    status_name = fields.String(validate=OneOf(["pending", "approved", "rejected"]))

    class Meta:
        # Fields to expose
        fields = ("id", "status_name", "leave_requests")

# To handle a single status object
status_schema = StatusSchema()

# To handle a list of status objects
statuses_schema = StatusSchema(many=True)