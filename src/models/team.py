from init import db, ma
from marshmallow import fields

class Team(db.Model):
    # Name of the table
    __tablename__ = "team"

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Relationships
    employees = db.relationship('Employee', back_populates='team')
    department = db.relationship('Department', back_populates='teams')

class TeamSchema(ma.Schema):
    # Nested relationship fields
    employees = fields.List(fields.Nested('EmployeeSchema', only=["first_name", "last_name"]))
    department = fields.Nested('DepartmentSchema', only=["department_name"])

    class Meta:
        # Fields to expose
        fields = ("id", "team_name", "department_id", "employees", "department")

# To handle a single team object
team_schema = TeamSchema()

# To handle a list of team objects
teams_schema = TeamSchema(many=True, exclude=["department_id", "employees"])