from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models import Employee, LeaveRequest, Status

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("seed")
def seed_tables():
    # Creates a list of Employee instances
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
            team_id = 1,
            email = "john.smith@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
        ),
        Employee(
            first_name = "Isidro",
            last_name = "Silva",
            team_id = 2,
            email = "isidro.silva@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8"),
            is_admin = True
        ), 
        Employee(
            first_name = "Parker",
            last_name = "Durham",
            team_id = 2,
            email = "parker.durham@email.com",
            password = bcrypt.generate_password_hash("q1w2e3").decode("utf-8")
        )
    ]

    db.session.add_all(employees)

    # References existing status names
    pending_status = Status.query.filter_by(status_name="Pending").first()
    approved_status = Status.query.filter_by(status_name="Approved").first()

    # Creates a list of LeaveRequest instances
    leave_requests = [
        LeaveRequest(
            start_date=date(2024, 10, 1),
            end_date=date(2024, 10, 4),
            employee=employees[0],  # Assign to Veronica
            status=pending_status   # Reference existing status
        ),
        LeaveRequest(
            start_date=date(2024, 11, 11),
            end_date=date(2024, 11, 15),
            employee=employees[1],  # Assign to John
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
    