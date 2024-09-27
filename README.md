# Annual Leave Tracker API - Veronica Chung T2A2

## Application Setup
Before running the application, you will need to install the necessary dependencies specified in the `requirements.txt` file.

1. Create and activate a virtual environment to keep the project's dependencies isolated.
`python -m venv .venv`
`source .venv/bin/activate`

2. Install the required packages.
`pip install -r requirements.txt`

## R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.
This Annual Leave Tracker API addresses significant challenges in managing employee leave in workplaces that rely on interdepartmental collaboration. Poor coordination of leave schedules can disrupt workflows and delay critical tasks, while a lack of visibility into colleagues' planned absences complicates project management. Many organisations still depend on manual processes like spreadsheets, which are prone to errors and lack real-time access to leave data. Additionally, manual approval systems often create bottlenecks, delaying important decisions and disrupting operations.

This API solves these issues by offering real-time visibility into approved leaves, facilitating better coordination across departments. With role-based access control, only authorised admin users can approve, modify or remove leave requests, which helps maintain data integrity. By centralising leave information, the API enables managers to make informed decisions and plan effectively around team availability, thus minimising disruptions to project timelines and enhancing overall efficiency.

## R2 Describe the way tasks are allocated and tracked in your project.


## R3 List and explain the third-party services, packages and dependencies used in this app.

**Flask==3.0.3:** Flask is a lightweight WSGI web application framework that simplifies routing and templating, making it ideal for efficiently building and managing the API.

**Flask-SQLAlchemy==3.1.1:** Integrates SQLAlchemy with Flask, providing a Pythonic ORM layer that simplifies database interactions and management of relational databases.

**Flask-JWT-Extended==4.6.0:** Enables JWT support in Flask applications, facilitating secure user authentication and protecting API endpoints by requiring valid tokens for access.

**Flask-Bcrypt==1.0.1:** Adds bcrypt hashing to the Flask app, enhancing password security by enabling the hashing and verification of passwords to protect user credentials from unauthorized access.

**flask-marshmallow==1.2.1:** Marshmallow is an object serialisation/deserialisation library that integrates with Flask to validate and convert complex data types, essential for managing API request and response formats.

**marshmallow-sqlalchemy==1.1.0:** Extends Marshmallow to seamlessly integrate with SQLAlchemy models, simplifying the serialisation and deserialisation of database models to JSON and vice versa, thus streamlining data preparation for API responses.

**psycopg2-binary==2.9.9:** Psycopg2 is the PostgreSQL adapter for Python. The -binary version is a self-contained package that simplifies the installation and use of PostgreSQL with Flask applications, enabling seamless database connectivity and operations.

**Werkzeug==3.0.3:** Werkzeug is a comprehensive WSGI web application library that serves as Flask's underlying toolkit, offering utilities and middleware components for effective request handling, debugging, and routing.

**greenlet==3.0.3:** Enables lightweight concurrency in Python by managing multiple threads of execution (greenlets), improving performance for I/O-bound applications like web servers.

**itsdangerous==2.2.0:** Safely signs data to ensure its integrity, and Flask uses it to securely manage sessions and cookies, protecting against tampering.

**Jinja2==3.1.4:** This is the templating engine for Python that Flask utilises to render HTML pages. While your API may not heavily rely on this for rendering, it is essential for any HTML responses or templates.

**MarkupSafe==2.1.5:** Escapes text to prevent injection attacks and is utilized by Jinja2 to ensure that data rendered in templates is safeguarded against XSS (Cross-Site Scripting) vulnerabilities.

**bcrypt==4.2.0:** Hashes passwords using the bcrypt algorithm, enhancing security by making it computationally expensive to reverse the hashes.

**click==8.1.7:** Creates CLI that Flask utilizes for its command-line utility, simplifying the execution of server commands and task management for developers.

**packaging==24.1:** Manages Python packages and versions, making it essential for ensuring compatibility and handling package dependencies.

**python-dotenv==1.0.1:** Manages environment variables through an .env file, allowing easy configuration of settings such as database URLs and API keys without hardcoding sensitive information.

**marshmallow==3.21.3:** Core serialisation/deserialisation library that provides the framework for converting complex data types into JSON-compatible formats and vice versa.

**typing_extensions==4.12.2:** Backports new type system features to be used in older Python versions.

## R4 Explain the benefits and drawbacks of this app’s underlying database system.
PostgreSQL is chosen as the database system for this API.

The advantages of using PostgreSQL include its adherence to ACID principles, which ensure the integrity, consistency, and reliability of transactions. This system also employs Multi-Version Concurrency Control (MVCC), allowing multiple transactions to occur simultaneously without locking the data, thus preventing conflicts and enhancing performance. PostgreSQL's extensibility permits users to create custom data types, operators, and functions, catering to specific project needs. Furthermore, it benefits from an active community that contributes to comprehensive documentation and regular updates, providing ongoing support.

Despite its strengths, PostgreSQL does have some drawbacks. It can be memory and CPU-intensive, which may lead to performance issues as data volume and complexity increase. The setup and configuration process can be intricate, especially for those looking to leverage its advanced capabilities, resulting in a steeper learning curve for beginners. Being an open-source database, there may be inconsistencies in user-friendly features or interfaces due to contributions from various communities, potentially leading to compatibility issues that require specific software or hardware.

## R5 Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.


## R6 Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.


## R7 Explain the implemented models and their relationships, including how the relationships aid the database implementation. This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.


## R8 Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:
* HTTP verb
* Path or route
* Any required body or header data
* Response
