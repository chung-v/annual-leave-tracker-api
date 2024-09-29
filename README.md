# Annual Leave Tracker API - Veronica Chung T2A2

## Application Setup
Before running the application, you will need to install PostgreSQL and the necessary dependencies specified in the `requirements.txt` file.

1. Start PostgreSQL. <br>
`sudo -u postgres psql`

2. Create a new user with a password. <br>
`CREATE USER {username} WITH PASSWORD '{password}';`

3. Create a new database. <br>
`CREATE DATABASE {database_name};`

4. Grant the user all privileges in the database. <br>
`GRANT ALL PRIVILEGES ON DATABASE {database_name} TO {username};`

5. Connect to the database <br>
`\c {database_name}`

6. Grant the user to use the public schema in the database. <br>
`GRANT USAGE ON SCHEMA public TO {username};`

7. Clone the repository. <br>
`git clone https://github.com/chung-v/veronicachung-t2a2.git`

8. Create and activate a virtual environment to keep the project's dependencies isolated. <br>
`python -m venv .venv` <br>
`source .venv/bin/activate`

9. Install the required packages. <br>
`pip install -r requirements.txt`

10. Create all database tables defined in the application. <br>
`flask db create`

11. Run the application. <br>
`flask run`

## R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.
This Annual Leave Tracker API addresses significant challenges in managing employee leave in workplaces that rely on interdepartmental collaboration. Poor coordination of leave schedules can disrupt workflows and delay critical tasks, while a lack of visibility into colleagues' planned absences complicates project management. Many organisations still depend on manual processes like spreadsheets, which are prone to errors and lack real-time access to leave data. Additionally, manual approval systems often create bottlenecks, delaying important decisions and disrupting operations.

This API solves these issues by offering real-time visibility into approved leaves, facilitating better coordination across departments. With role-based access control, only authorised admin users can approve, modify or remove leave requests, which helps maintain data integrity. By centralising leave information, the API enables managers to make informed decisions and plan effectively around team availability, thus minimising disruptions to project timelines and enhancing overall efficiency.

## R2 Describe the way tasks are allocated and tracked in your project.
Trello was employed for project planning and task management. Each task featured a checklist to guarantee that all elements of the project were addressed. Tasks were prioritised depending on the significance of the files necessary to operate the application.

### Progress made by 17/09/24
![Trello progress on 17/09/24](/doc/trello_1.png)

### Progress made by 22/09/24
![Trello progress on 12/09/24](/doc/trello_2.png)

### Progress made by 24/09/24
![Trello progress on 14/09/24](/doc/trello_3.png)

### Progress made by 29/09/24
![Trello progress on 29/09/24](/doc/trello_4.png)

## R3 List and explain the third-party services, packages and dependencies used in this app.

- **bcrypt==4.2.0:** Hashes passwords using the bcrypt algorithm, enhancing security by making it computationally expensive to reverse the hashes.

- **click==8.1.7:** Creates CLI that Flask utilises for its command-line utility, simplifying the execution of server commands and task management for developers.

- **Flask==3.0.3:** Flask is a lightweight WSGI web application framework that simplifies routing and templating, making it ideal for efficiently building and managing the API.

- **Flask-Bcrypt==1.0.1:** Adds bcrypt hashing to the Flask app, enhancing password security by enabling the hashing and verification of passwords to protect user credentials from unauthorised access.

- **Flask-JWT-Extended==4.6.0:** Enables JWT support in Flask applications, facilitating secure user authentication and protecting API endpoints by requiring valid tokens for access.

- **flask-marshmallow==1.2.1:** Marshmallow is an object serialisation/deserialisation library that integrates with Flask to validate and convert complex data types, essential for managing API request and response formats.

- **Flask-SQLAlchemy==3.1.1:** Integrates SQLAlchemy with Flask, providing a Pythonic ORM layer that simplifies database interactions and management of relational databases.

- **greenlet==3.0.3:** Enables lightweight concurrency in Python by managing multiple threads of execution (greenlets), improving performance for I/O-bound applications like web servers.

- **itsdangerous==2.2.0:** Safely signs data to ensure its integrity, and Flask uses it to securely manage sessions and cookies, protecting against tampering.

- **Jinja2==3.1.4:** This is the templating engine for Python that Flask utilises to render HTML pages. While your API may not heavily rely on this for rendering, it is essential for any HTML responses or templates.

- **MarkupSafe==2.1.5:** Escapes text to prevent injection attacks and is utilised by Jinja2 to ensure that data rendered in templates is safeguarded against XSS (Cross-Site Scripting) vulnerabilities.

- **marshmallow==3.21.3:** Core serialisation/deserialisation library that provides the framework for converting complex data types into JSON-compatible formats and vice versa.

- **marshmallow-sqlalchemy==1.1.0:** Extends Marshmallow to seamlessly integrate with SQLAlchemy models, simplifying the serialisation and deserialisation of database models to JSON and vice versa, thus streamlining data preparation for API responses.

- **packaging==24.1:** Manages Python packages and versions, making it essential for ensuring compatibility and handling package dependencies.

- **psycopg2-binary==2.9.9:** Psycopg2 is the PostgreSQL adapter for Python. The -binary version is a self-contained package that simplifies the installation and use of PostgreSQL with Flask applications, enabling seamless database connectivity and operations.

- **python-dotenv==1.0.1:** Manages environment variables through an .env file, allowing easy configuration of settings such as database URLs and API keys without hardcoding sensitive information.

- **SQLAlchemy==2.0.32:** SQL toolkit and ORM library for Python, enabling efficient database interaction and management in the application.

- **typing_extensions==4.12.2:** Backports new type system features to be used in older Python versions.

- **Werkzeug==3.0.3:** Werkzeug is a comprehensive WSGI web application library that serves as Flask's underlying toolkit, offering utilities and middleware components for effective request handling, debugging, and routing.

## R4 Explain the benefits and drawbacks of this app’s underlying database system.
PostgreSQL is used as the database system for this API. The advantages of using PostgreSQL include its adherence to ACID principles, which ensure the integrity, consistency, and reliability of transactions. This system also employs Multi-Version Concurrency Control (MVCC), allowing multiple transactions to occur simultaneously without locking the data, thus preventing conflicts and enhancing performance. PostgreSQL's extensibility permits users to create custom data types, operators, and functions, catering to specific project needs. Furthermore, it benefits from an active community that contributes to comprehensive documentation and regular updates, providing ongoing support.

Despite its strengths, PostgreSQL does have some drawbacks. It can be memory and CPU-intensive, which may lead to performance issues as data volume and complexity increase. The setup and configuration process can be intricate, especially for those looking to leverage its advanced capabilities, resulting in a steeper learning curve for beginners. Being an open-source database, there may be inconsistencies in user-friendly features or interfaces due to contributions from various communities, potentially leading to compatibility issues that require specific software or hardware.

## R5 Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.
### Purpose and Functionalities
This application was built using SQLAlchemy as the Object-Relational Mapping (ORM) system. It bridges the gap between Python application code and relational databases, fostering a clearer coding approach for developers by interacting with the database using Python objects instead of raw SQL queries. SQLAlchemy simplifies interactions with the database and enhances code readability and maintainability.

### Features
**Models**: SQLAlchemy allows the definition of models where database tables like `Employee` are represented as Python classes. Each class attribute corresponds to a column in the database table, making it easy to define the structure of your data and its types. This provides a clear and structured way to interact with the database.

    class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

**Relationships**: SQLAlchemy simplifies handling relationships between tables by allowing the user to define relationships directly in their models. This enables easy access to related data, making it intuitive to navigate between entities. In the below example, the relationship between `Employee` and `Team` is established through a foreign key, allowing you to fetch all employees belonging to a specific team without writing complex join queries.

    team = db.relationship('Team', back_populates='employees')

**Foreign Keys**: Foreign keys are used to define the relationships between different entities, enhancing data integrity and relational organisation. By using foreign keys, SQLAlchemy ensures that the relationships between tables are maintained correctly, preventing orphaned records and maintaining referential integrity. This is crucial for data consistency in a relational database.

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

**CRUD Operations**: SQLAlchemy provides a straightforward way to perform CRUD (Create, Read, Update, and Delete) operations on your database. This allows developers to interact with the database easily without having to write complex SQL queries.

    # View a list of all departments
    @department_bp.route("/list", methods=['GET'])
    @jwt_required()
    def get_all_departments():
        stmt = db.select(Department).order_by(Department.department_name.asc())
        departments = db.session.scalars(stmt)
        return departments_schema.dump(departments), 200

**Querying**: SQLAlchemy enables robust querying capabilities to retrieve all entries or filter results based on specific conditions. This makes it simple to fetch data according to the needs of the application, whether you are looking for a single record or a list of records that match certain criteria.

    # Fetch leave requests with the "pending" status
    pending_status = db.session.query(Status).filter(Status.status_name == "pending").first()

**Schema Validation**: SQLAlchemy enforces data integrity through schema validation, using column constraints like `NOT NULL` and `UNIQUE`. These constraints ensure that valid data is entered into the database, preventing issues related to invalid or duplicate entries.

    email = db.Column(db.String(100), unique=True, nullable=False)  # Ensures email is unique and not null

## R6 Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

![Annual Leave Tracker ERD](/doc/ERD.png)

The ERD outlines a normalised database design for an employee leave tracking system, comprising five key entities: `Employee`, `LeaveRequest`, `Status`, `Team`, and `Department`. These relationships are designed in Third Normal Form (3NF), ensuring that data is well-structured and efficiently managed. Each entity focuses on a specific concept, like employees or teams, with foreign keys linking them together. This normalisation prevents data redundancy by storing information such as team names or status labels in separate tables and referencing them through foreign keys. For example, `LeaveRequest` links to `Status` through `status_id` to avoid repeating status names in every leave request.

The use of foreign key relationships between these models enforces data integrity and ensures consistency across the database. Relationships such as `Employee-LeaveRequest` and `Team-Employee` guarantee that employees belong to valid teams and that leave requests are associated with legitimate employees, improving data accuracy. The design also allows for efficient data retrieval through SQL joins, enabling fast queries across tables, such as fetching all leave requests for a particular team or department.

The structured relationships between the models in the ERD enhance the database design by ensuring data integrity, reducing redundancy, improving query performance, and facilitating maintainability. By implementing a clear, normalised design, the database becomes more scalable, easier to extend, and better equipped to handle complex queries and business logic while maintaining efficiency and consistency.

## R7 Explain the implemented models and their relationships, including how the relationships aid the database implementation. This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.
The implemented models in the project include `Employee`, `LeaveRequest`, `Status`, `Team`, and `Department`, each representing a table in the database. The relationships between these models follow typical one-to-many and many-to-one patterns to efficiently manage the application's data.

**Employee Model**: Stores employee details, such as `first_name`, `email`, and a foreign key `team_id` linking to the `Team` model. This establishes a many-to-one relationship, where multiple employees can belong to one team.

    class Employee(db.Model):
        # Name of the table
        __tablename__ = "employee"

        # Attributes of the table
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(100), nullable=False)
        team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)

        # Relationships
        team = db.relationship('Team', back_populates='employees')
        leave_requests = db.relationship('LeaveRequest', back_populates='employee')

**LeaveRequest Model**: Captures the details of leave requests, including `employee_id` (foreign key to `Employee`), `status_id` (foreign key to `Status`), and start and end dates. The many-to-one relationship with `Employee` ensures each leave request is associated with a specific employee, while the relationship with `Status` tracks the current state of the leave request.

    class LeaveRequest(db.Model):
        # Name of the table
        __tablename__ = "leave_request"

        # Attributes of the table
        id = db.Column(db.Integer, primary_key=True)
        employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
        start_date = db.Column(db.Date, nullable=False)
        end_date = db.Column(db.Date, nullable=False)
        status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

        employee = db.relationship('Employee', back_populates='leave_requests')
        status = db.relationship('Status', back_populates='leave_requests')

**Team and Department Models**: A many-to-one relationship between `Team` and `Department` ensures that each team is linked to a specific department, allowing for organised data retrieval and reporting.

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

    class Department(db.Model):
        # Name of the table
        __tablename__ = "department"

        # Attributes of the table
        id = db.Column(db.Integer, primary_key=True)
        department_name = db.Column(db.String(100), nullable=False, unique=True)

        # Relationships
        teams = db.relationship('Team', back_populates='department')

**Status Model**: Defines different statuses for leave requests (e.g. pending, approved), linked through a foreign key in `LeaveRequest`. This allows the system to manage leave request workflows by updating status IDs.

    class Status(db.Model):
        # Name of the table
        __tablename__ = "status"

        # Attributes of the table
        id = db.Column(db.Integer, primary_key=True)
        status_name = db.Column(db.String, nullable=False, unique=True)

        # Relationships
        leave_requests = db.relationship('LeaveRequest', back_populates='status')

## R8 Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:
* #### HTTP verb
* #### Path or route
* #### Any required body or header data
* #### Response <br>

### Authentication Routes
#### 1. /auth/register
Description: Register a new employee.
HTTP verb: POST
Required header: None

**Successful response:**
![Successful response: /auth/register](/doc/auth_controller/auth_1a.png)
Account is created and employee information is displayed.

**Failed response:**
![Failed response: /auth/register](/doc/auth_controller/auth_1b.png)
Prevents duplicate accounts.

![Failed response: /auth/register](/doc/auth_controller/auth_1c.png)
Password has a minimum length for data security.

![Failed response: /auth/register](/doc/auth_controller/auth_1d.png)
Required attributes must be filled.

#### 2. /auth/login
Description: Login an existing employee.
HTTP verb: POST
Required header: None

**Successful response:**
![Successful response: /auth/login](/doc/auth_controller/auth_2a.png)
Employee is logged in and JWT is created. This expires in 1 day. Employee can also see if they have admin rights.

**Failed response:**
![Failed response: /auth/login](/doc/auth_controller/auth_2b.png)
Correct email and password is required to login.

#### 3. /auth/update
Description: Update employee details - first name, last name or password.
HTTP verb: PUT, PATCH
Required header: @jwt_required()

**Successful response:**
![Successful response: /auth/update](/doc/auth_controller/auth_3a.png)
Employee information is updated and displayed.

**Failed response:**
![Failed response: /auth/update](/doc/auth_controller/auth_3b.png)
Employees without admin rights can only update their name and password, for data accuracy.

#### 4. /auth/update/<int:employee_id>
Description: Update employee details (admin only) - first name, last name, email, or team ID.
HTTP verb: PUT, PATCH
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /auth/update/<int:employee_id>](/doc/auth_controller/auth_4a.png)
Employee information is updated and displayed for the admin.

**Failed response:**
![Failed response: /auth/update/<int:employee_id>](/doc/auth_controller/auth_4b.png)
Department ID cannot be manually changed as it is linked to the Team ID.

![Failed response: /auth/update/<int:employee_id>](/doc/auth_controller/auth_4c.png)
Employees without admin rights cannot access the route.

#### 5. /auth/delete/<int:employee_id>
Description: Delete employee (admin only)
HTTP verb: DELETE
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /auth/delete/<int:employee_id>](/doc/auth_controller/auth_5a.png)
Employee is removed from the database.

**Failed response:**
![Failed response: /auth/delete/<int:employee_id>](/doc/auth_controller/auth_5b.png)
Error message if employee does not exist on the database.

#### 6. /auth/admin/<int:employee_id>
Description: Add employee as admin
HTTP verb: POST
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_6a.png)
Employee becomes an admin.

**Failed response:**
![Failed response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_6b.png)
Prevents admins being added as an admin again.

![Failed response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_6c.png)
Only Employee IDs that exist in the database can be added as an admin.

#### 7. /auth/admin/<int:employee_id>
Description: Delete employee as admin
HTTP verb: DELETE
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_7a.png)
Employee no longer is an admin.

**Failed response:**
![Failed response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_7b.png)
Regular employees cannot be removed as admin.

![Failed response: /auth/admin/<int:employee_id>](/doc/auth_controller/auth_7c.png)
Only Employee IDs that exist in the database can be removed from admin rights.

### Department Routes
#### 1. /department/list
Description: View a list of all departments
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /department/list](/doc/dept_controller/dept_3a.png)
A list containing all departments within the database is displayed.

**Failed response:**
![Failed response: /department/list](/doc/dept_controller/dept_3b.png)
JWT token is required to view the list for data security.

#### 2. /department/add
Description: Create a new department (admin only)
HTTP verb: POST
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /department/add](/doc/dept_controller/dept_1a.png)
Department is added to the database.

**Failed response:**
![Failed response: /department/add](/doc/dept_controller/dept_1b.png)
Prevents departments from being duplicated.

#### 3. /department/delete/<int:department_id>
Description: Delete a department (admin only)
HTTP verb: DELETE
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /department/delete/<int:department_id>](/doc/dept_controller/dept_2a.png)
Department is removed from the database.

**Failed response:**
![Failed response: /department/delete/<int:department_id>](/doc/dept_controller/dept_2b.png)
Only Department IDs that exist in the database can be removed.

### Team Routes
#### 1. /team/list
Description: View a list of all teams
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /team/list](/doc/team_controller/team_1a.png)
A list containing all teams and the department they belong to is displayed.

**Failed response:**
![Failed response: /team/list](/doc/team_controller/team_1b.png)
JWT token is required to view the list for data security.


#### 2. /team/list/<int:team_id>
Description: View approved leave in upcoming month for a specific team
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /team/list/<int:team_id>](/doc/team_controller/team_2a.png)
Approved leave for the upcoming month is displayed for the selected team.

**Failed response:**
![Failed response: /team/list/<int:team_id>](/doc/team_controller/team_2b.png)
Message is displayed when there is no approved or planned leave in the next month.

#### 3. /team/add
Description: Create a new team (admin only)
Required header: @jwt_required(), @auth_as_admin_decorator
HTTP verb: POST

**Successful response:**
![Successful response: /team/add](/doc/team_controller/team_3a.png)
Team is added to the database.

**Failed response:**
![Failed response: /team/add](/doc/team_controller/team_3b.png)
Department ID must be entered as each team falls under a department.

#### 4. /team/delete/<int:team_id>
Description: Delete a team (admin only)
HTTP verb: DELETE
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /team/delete/<int:team_id>](/doc/team_controller/team_4a.png)
Team is removed from the database.

**Failed response:**
![Failed response: /team/delete/<int:team_id>](/doc/team_controller/team_4b.png)
Only Team IDs that exist in the database can be removed.

### Employee Routes
#### 1. /employee/<int:employee_id>
Description: View approved leave in the upcoming month for a specific employee
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /employee/<int:employee_id>](/doc/emp_controller/emp_1a.png)
Approved leave for the upcoming month is displayed for the selected employee.

**Failed response:**
![Failed response: /employee/<int:employee_id>](/doc/emp_controller/emp_1b.png)
Message is displayed when there is no approved or planned leave in the next month.

#### 2. /employee/list
Description: Get a list of all employees (admin only)
HTTP verb: GET
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /employee/list](/doc/emp_controller/emp_2a.png)
A list containing all employees in the database is displayed.

**Failed response:**
![Failed response: /employee/list](/doc/emp_controller/emp_2b.png)
JWT token is required to view the list for data security.

### Leave Request Routes
#### 1. /leave_request
Description: View all leave requests for self
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /leave_request](/doc/lr_controller/lr_1a.png)
A list containing all leave requests and their status are displayed.

**Failed response:**
![Failed response: /leave_request](/doc/lr_controller/lr_1b.png)
Message is displayed when there is no leave requests submitted.

#### 2. /leave_request/<int:leave_request_id>
Description: View specific leave request for self
HTTP verb: GET
Required header: @jwt_required()

**Successful response:**
![Successful response: /leave_request/<int:leave_request_id>](/doc/lr_controller/lr_2a.png)
Details on a specific leave request and its status is displayed.

**Failed response:**
![Failed response: /leave_request/<int:leave_request_id>](/doc/lr_controller/lr_2b.png)
Only Leave Request IDs that exist in the database and belongs to the employee can be viewed.

#### 3. /leave_request/add
Description: Add new leave request
HTTP verb: POST
Required header: @jwt_required()

**Successful response:**
![Successful response: /leave_request/add](/doc/lr_controller/lr_3a.png)
New leave request is submitted and status is set to "pending".

**Failed response:**
![Failed response: /leave_request/add](/doc/lr_controller/lr_3b.png)
Prevents duplicate leave requests to be submitted.

#### 4. /leave_request/delete/<int:leave_request_id>
Description: Delete leave request
HTTP verb: DELETE
Required header: @jwt_required()

**Successful response:**
![Successful response: /leave_request/delete/<int:leave_request_id>](/doc/lr_controller/lr_4a.png)
Leave Request ID is removed from database.

**Failed response:**
![Failed response: /leave_request/delete/<int:leave_request_id>](/doc/lr_controller/lr_4b.png)
Only Leave Request IDs that exist in the database and belongs to the employee can be removed.

#### 5. /leave_request/approve/<int:leave_request_id>
Description: Approve leave request (admin only)
HTTP verb: POST
Required header: @jwt_required(), @auth_as_admin_decorator

**Successful response:**
![Successful response: /leave_request/approve/<int:leave_request_id>](/doc/lr_controller/lr_5a.png)
Leave request status is updated from "pending" to "approved".

**Failed response:**
![Failed response: /leave_request/approve/<int:leave_request_id>](/doc/lr_controller/lr_5b.png)
Only Leave Request IDs that exist in the database and is "pending" can be approved.