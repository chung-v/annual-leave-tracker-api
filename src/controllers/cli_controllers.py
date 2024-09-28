from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models import Employee, Department, Team, Status, LeaveRequest

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create a list of Department instances
    departments = [
        Department(name="Human Resources"),
        Department(name="Marketing"),
        Department(name="IT")
    ]
    
    # Add and commit departments to the database
    db.session.add_all(departments)
    db.session.commit()  # Commit to save department records before referencing them in Team instances

    # Create a list of Team instances
    teams = [
        Team(name="Recruitment Team", department_id=1),
        Team(name="Project Management Team", department_id=2),
        Team(name="Customer Relationship Management Team", department_id=2),
        Team(name="Development Team", department_id=3)
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
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
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
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
        ),
        Employee(
            first_name = "Parker",
            last_name = "Durham",
            team_id = 4,
            email = "parker.durham@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
            is_admin = True
        ),
        Employee(
            first_name = "Sue",
            last_name = "Joseph",
            team_id = 4,
            email = "sue.joseph@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
        )
    ]

    db.session.add_all(employees)

    # Reference existing status names
    pending_status = Status.query.filter_by(status_name="Pending").first()
    approved_status = Status.query.filter_by(status_name="Approved").first()

    # Create a list of LeaveRequest instances
    leave_requests = [
        LeaveRequest(
            start_date=date(2024, 10, 1),
            end_date=date(2024, 10, 4),
            employee=employees[3],  # Assign to Cecelia
            status=pending_status   # Reference existing status
        ),
        LeaveRequest(
            start_date=date(2024, 11, 11),
            end_date=date(2024, 11, 15),
            employee=employees[5],  # Assign to Sue
            status=approved_status  # Reference existing status
        )
    ]

    db.session.add_all(leave_requests)

    db.session.commit()

    print("Tables seeded.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")
    