from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.employee import Employee
from models.leave_request import LeaveRequest, leave_requests_schema
from models.department import Department
from models.team import Team, teams_schema, team_schema
from models.status import Status
from utils import auth_as_admin_decorator

team_bp = Blueprint("team", __name__, url_prefix="/team")

# Create a new team (admin only)
@team_bp.route('/add', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def create_team():
    # Get the data from the body of the request
    team_data = team_schema.load(request.get_json())

    # Ensure the department_id is provided in the request
    department_id = team_data.get("department_id")
    if not department_id:
        return {"error": "Department ID is required."}, 400
    
    # Verify if the department exists
    department = db.session.get(Department, department_id)
    if not department:
        return {"error": f"Department ID {department_id} does not exist."}, 404

    # Create a new team model instance
    team = Team(
        team_name=team_data.get("team_name"),
        department_id=department_id
    )
    # Add and commit to the DB
    db.session.add(team)
    db.session.commit()
    # Response message
    return team_schema.dump(team), 201

# Delete a team (admin only)
@team_bp.route("/delete/<int:team_id>", methods=["DELETE"])
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
        return {"message": f"Team ID {team_id} ({team.team_name}) deleted successfully."}, 200
    else:
        # Return error message
        return {"error": f"Team ID {team_id} not found."}, 404

# Get a list of all teams
@team_bp.route("/list", methods=["GET"])
def get_all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc())
    teams = db.session.scalars(stmt)
    return teams_schema.dump(teams), 200

# View approved leave in upcoming month for a specific team
@team_bp.route("/leaves/<int:team_id>", methods=["GET"])
@jwt_required()
def view_approved_leaves_in_team(team_id):
    # Get the current date and the date 30 days from today
    start_date = datetime.today()
    end_date = start_date + timedelta(days=30)

    # Verify if the team exists
    team = db.session.get(Team, team_id)
    if not team:
        return {"error": f"Team with ID {team_id} not found."}, 404

    # Retrieve the "approved" status ID from the Status table
    approved_status = db.session.query(Status).filter(Status.status_name == "approved").first()

    # Query for approved leave requests for employees in the specified team within the next 30 days
    leaves_stmt = db.select(LeaveRequest).join(Employee).filter(
        Employee.team_id == team_id,
        LeaveRequest.status_id == approved_status.id,
        LeaveRequest.start_date.between(start_date, end_date)
    )
    approved_leaves = db.session.execute(leaves_stmt).scalars().all()

    # Check if any approved leaves were found
    if not approved_leaves:
        return {"message": f"No approved leave requests found for team ID {team_id} in the upcoming month."}, 404

    # Return the approved leaves
    return leave_requests_schema.dump(approved_leaves), 200
