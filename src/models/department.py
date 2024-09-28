from init import db, ma
from marshmallow import fields

class Department(db.Model):
    # Name of the table
    __tablename__ = "department"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationships
    teams = db.relationship('Team', back_populates='department')

class DepartmentSchema(ma.Schema):
    # Nested relationship field
    teams = fields.List(fields.Nested('TeamSchema', exclude=["department"]))

    class Meta:
        # Fields to expose
        fields = ("id", "department_name", "teams")

# To handle a single department object
department_schema = DepartmentSchema()

# To handle a list of department objects
departments_schema = DepartmentSchema(many=True)
