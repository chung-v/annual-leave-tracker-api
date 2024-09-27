# Annual Leave Tracker API - Veronica Chung T2A2

## Application Setup
Before running the application, you will need to install the necessary dependencies specified in the `requirements.txt` file.

1. Create and activate a virtual environment to keep your project's dependencies isolated.
`python -m venv .venv`
`source .venv/bin/activate`

2. Install the required packages.
`pip install -r requirements.txt`

## R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.
This Annual Leave Tracker API addresses significant challenges in managing employee leave in workplaces that rely on interdepartmental collaboration. Poor coordination of leave schedules can disrupt workflows and delay critical tasks, while a lack of visibility into colleagues' planned absences complicates project management. Many organisations still depend on manual processes like spreadsheets, which are prone to errors and lack real-time access to leave data. Additionally, manual approval systems often create bottlenecks, delaying important decisions and disrupting operations.

This API solves these issues by offering real-time visibility into approved leaves, facilitating better coordination across departments. With role-based access control, only authorised admin users can approve, modify or remove leave requests, which helps maintain data integrity. By centralising leave information, the API enables managers to make informed decisions and plan effectively around team availability, thus minimising disruptions to project timelines and enhancing overall efficiency.

## R2 Describe the way tasks are allocated and tracked in your project.


## R3 List and explain the third-party services, packages and dependencies used in this app.

**Flask==3.0.3:** Flask is a lightweight WSGI web application framework that allows for easy routing and templating. It serves as the core framework for building your API, enabling you to handle HTTP requests and manage application structure effectively.

**Flask-SQLAlchemy==3.1.1:** This package integrates SQLAlchemy with Flask, simplifying database interactions. It provides an ORM (Object-Relational Mapping) layer to manage database operations in a more Pythonic way, making it easier to work with relational databases.

**Flask-JWT-Extended==4.6.0:** This extension provides support for JSON Web Tokens (JWT) in Flask applications, allowing for secure user authentication. It helps manage user sessions and protects API endpoints by requiring valid tokens for access.

**Flask-Bcrypt==1.0.1:** This package adds bcrypt hashing to your Flask app, enhancing password security. It allows for hashing and verifying passwords, helping to protect user credentials against unauthorised access.

**flask-marshmallow==1.2.1:** Marshmallow is an object serialisation/deserialisation library that integrates with Flask to validate and convert complex data types to and from Python data types. This is crucial for handling API request and response formats.

**marshmallow-sqlalchemy==1.1.0:** This package extends Marshmallow to work seamlessly with SQLAlchemy models, allowing for easier serialisation and deserialisation of database models to JSON and vice versa. It simplifies the process of preparing data for API responses.

**psycopg2-binary==2.9.9:** Psycopg2 is the PostgreSQL adapter for Python. The -binary version is a self-contained package that makes it easier to install and use PostgreSQL with Flask applications, enabling database connectivity and operations.

**Werkzeug==3.0.3:** Werkzeug is a comprehensive WSGI web application library that Flask uses as its underlying toolkit. It provides various utilities and middleware components that facilitate request handling, debugging, and routing.

**greenlet==3.0.3:** This library is used for lightweight concurrency in Python. It provides the ability to manage multiple threads of execution (greenlets), which can enhance performance for I/O-bound applications like web servers.

**itsdangerous==2.2.0:** A utility for safely signing data to ensure its integrity. Flask uses this for securely handling sessions and cookies, protecting against tampering.

**Jinja2==3.1.4:** This is the templating engine for Python that Flask utilises to render HTML pages. While your API may not heavily rely on this for rendering, it is essential for any HTML responses or templates.

**MarkupSafe==2.1.5:** This package provides a way to escape text to prevent injection attacks. It is used by Jinja2 to ensure that data rendered in templates is safe from XSS (Cross-Site Scripting) vulnerabilities.

**bcrypt==4.2.0:** A library for hashing passwords using the bcrypt algorithm, enhancing security by making it computationally expensive to reverse hashes.

**click==8.1.7:** Click is a package for creating command-line interfaces (CLI). Flask uses it for its command-line utility, allowing developers to run server commands and manage tasks more easily.

**packaging==24.1:** A library that provides utilities for dealing with Python packages and versions. It is essential for ensuring compatibility and managing package dependencies.

**python-dotenv==1.0.1:** This package helps manage environment variables through a .env file, allowing for the easy configuration of settings such as database URLs and API keys without hardcoding sensitive information.

**marshmallow==3.21.3:** The core serialisation/deserialisation library that provides the framework for converting complex data types into JSON-compatible formats and vice versa.

**typing_extensions==4.12.2:** This package provides backports of the standard library's typing module, offering type hints and annotations that improve code clarity and support type checking.

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
