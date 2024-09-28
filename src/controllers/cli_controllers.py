from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.department import Department
from models.team import Team
from models.employee import Employee
from models.status import Status, VALID_STATUSES
from models.leave_request import LeaveRequest

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create a list of Department instances
    departments = [
        Department(department_name="Human Resources"),
        Department(department_name="Marketing"),
        Department(department_name="IT")
    ]
    
    # Add and commit departments to the database
    db.session.add_all(departments)
    db.session.commit()  # Commit to save department records before referencing them in Team instances

    # Create a list of Team instances
    teams = [
        Team(team_name="Recruitment Team", department_id=1),
        Team(team_name="Project Management Team", department_id=2),
        Team(team_name="Customer Relationship Management Team", department_id=2),
        Team(team_name="Development Team", department_id=3)
    ]

    # Add and commit teams to the database
    db.session.add_all(teams)
    db.session.commit() # Commit to save team records before referencing them in Employee instances
    
    # Create a list of Employee instances
    employees = [
        Employee(
            first_name = "Veronica",
            last_name = "Chung",
            team_id = 1,
            email = "veronica.chung@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
            is_admin = True
        ), 
        Employee(
            first_name = "John",
            last_name = "Smith",
            team_id = 2,
            email = "john.smith@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
            is_admin = True
        ),
        Employee(
            first_name = "Isidro",
            last_name = "Silva",
            team_id = 3,
            email = "isidro.silva@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
            is_admin = True
        ), 
        Employee(
            first_name = "Cecelia",
            last_name = "Woodward",
            team_id = 3,
            email = "cecelia.woodward@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
        ),
        Employee(
            first_name = "Parker",
            last_name = "Durham",
            team_id = 4,
            email = "parker.durham@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
            is_admin = True
        ),
        Employee(
            first_name = "Sue",
            last_name = "Joseph",
            team_id = 4,
            email = "sue.joseph@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
        )
    ]

    db.session.add_all(employees)

    # Create a list of Status instances
    statuses = [Status(status_name=status) for status in VALID_STATUSES]

    db.session.add_all(statuses)
    db.session.commit()

    # Create a list of LeaveRequest instances
    leave_requests = [
        LeaveRequest(
            start_date=date(2024, 10, 1),
            end_date=date(2024, 10, 4),
            employee=employees[3],  # Assign to Cecelia
            status=statuses[0]      # Pending
        ),
        LeaveRequest(
            start_date=date(2024, 11, 11),
            end_date=date(2024, 11, 15),
            employee=employees[5],  # Assign to Sue
            status=statuses[1]      # Approved
        ),
        LeaveRequest(
            start_date=date(2024, 11, 25),
            end_date=date(2024, 11, 27),
            employee=employees[5],  # Assign to Sue
            status=statuses[2]      # Rejected
        )
    ]

    db.session.add_all(leave_requests)
    db.session.commit()

    print("Tables seeded.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")
