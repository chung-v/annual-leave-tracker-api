from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.employee import Employee, employees_schema
from models.leave_request import LeaveRequest, leave_request_schema
from models.team import Team, teams_schema, team_schema
from utils import auth_as_admin_decorator

team_bp = Blueprint("team", __name__, url_prefix="/team")

# Get a list of all teams
@team_bp.route("/", methods=["GET"])
def get_all_teams():
    stmt = db.select(Team).order_by(Team.name.asc())
    teams = db.session.scalars(stmt).all()
    return teams_schema.dump(teams), 200

# Create a new team
@team_bp.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def create_team():
    # Get the data from the body of the request
    team_data = team_schema.load(request.get_json())
    # Create a new team model instance
    team = Team(
        name=team_data.get("name"),
        description=team_data.get("description")
    )
    # Add and commit to the DB
    db.session.add(team)
    db.session.commit()
    # Response message
    return team_schema.dump(team), 201

# Delete a team
@team_bp.route("/<int:team_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_team(team_id):
    # Fetch the team from the database
    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)
    # If team exists
    if team:
        # Delete the team
        db.session.delete(team)
        db.session.commit()
        return {"message": f"Team {team.name} deleted successfully."}, 200
    else:
        # Return error message
        return {"error": f"Team ID {team_id} not found."}, 404

# View approved leave in upcoming month for a specific team
@team_bp.route("/<int:team_id>", methods=["GET"])
@jwt_required()
def view_approved_leaves_in_team(team_id):
    start_date = datetime.today()
    end_date = start_date + timedelta(days=30)
    
    # Check if the team exists
    employees = db.session.execute(
        db.select(Employee).filter_by(team_id=team_id)
    ).scalars().all()

    if not employees:
        return {"error": f"Team ID {team_id} not found."}, 404

    # Loop through the employees and get their approved leave requests
    team_approved_leaves = []

    for employee in employees:
        employee_data = employees_schema.dump(employee)

        leaves = db.session.execute(
            db.select(LeaveRequest).filter(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.status == 'approved',
                LeaveRequest.start_date.between(start_date, end_date)
            )
        ).scalars().all()

        employee_data['approved_leaves'] = leave_request_schema.dump(leaves, many=True, exclude=['id'])
        team_approved_leaves.append(employee_data)

    # Return approved leaves or error if no leaves are found
    if not team_approved_leaves:
        return {"message": f"No approved leave requests found for team ID {team_id} in the upcoming month."}, 404

    # Return the list of approved leaves
    return team_approved_leaves, 200
