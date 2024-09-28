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
    department = db.relationship('Department', back_populates='teams')
    employees = db.relationship('Employee', back_populates='team')

class TeamSchema(ma.Schema):
    # Nested relationship fields
    employees = fields.List(fields.Nested('EmployeeSchema', exclude=["team"]))
    department = fields.Nested('DepartmentSchema', exclude=["teams"])

    class Meta:
        # Fields to expose
        fields = ("id", "team_name", "department_id", "employees", "department")

# to handle a single team object
team_schema = TeamSchema()

# to handle a list of team objects
teams_schema = TeamSchema(many=True)
