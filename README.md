# Event Ticketing Service

```bash
   ______                 __     _______      __        __  _
   / ____/   _____  ____  / /_   /_  __(_)____/ /_____  / /_(_)___  ____ _
  / __/ | | / / _ \/ __ \/ __/    / / / / ___/ //_/ _ \/ __/ / __ \/ __ `/
 / /___ | |/ /  __/ / / / /_     / / / / /__/ ,< /  __/ /_/ / / / / /_/ /
/_____/ |___/\___/_/ /_/\__/    /_/ /_/\___/_/|_|\___/\__/_/_/ /_/\__, /
                                                                 /____/


--- Event Ticketing CLI ---
1: List Events
2: Create Event
3: Delete Event
4: List Users
5: Create User
6: Delete User
7: Create Reservation
8: Update Reservation
9: Delete Reservation
10: Get User Reservations
11: Lookup Reservation
12: Exit
Enter choice:
```

This project is an event ticketing service built with FastAPI and MySQL. It allows users to view events, make reservations for tickets, and manage their reservations, etc.

This service also stands out for its ability to handle multiple requests concurrently, ensuring high performance and responsiveness even under load. Ideal for event organizers and platforms looking for a scalable ticket reservation system.

## Features

- Asynchronous Core: Utilizes FastAPI's asynchronous capabilities to manage event listings, ticket reservations, and user interactions without blocking, ensuring swift response times.
- CRUD Operations: Supports Create, Read, Update, and Delete (CRUD) operations for events, users, and reservations, providing a comprehensive management system.
- Concurrency Handling: Designed to handle multiple ticket reservations and queries concurrently, preventing double bookings and enhancing user experience.
- Data Validation: Implements rigorous input validation to ensure data integrity and provide informative feedback for API consumers.
- Docker Integration: Comes with a Dockerfile and docker-compose.yaml for easy deployment and environment setup, ensuring consistency across different setups.
- User and Reservation Management: Offers detailed user management and the ability to view all reservations, enhancing administrative capabilities.

## Technologies

- FastAPI
- MySQL
- Pydantic
- SQLAlchemy (AsyncIO Edition)
- Sqlmodel
- Docker

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installing

1. Clone the repository:

```bash
$ git clone git@github.com:ken1009us/event-ticketing-service.git
```

2. Navigate to the project directory:

```bash
$ cd event-ticketing-service
```

3. Start the application with Docker Compose:

Make sure you have `.env` file to store your required environment variables:

```bash
DB_HOST={DB_HOST}
DB_NAME={DB_NAME}
DB_USER={DB_USER}
DB_PASSWORD={DB_PASSWORD}
MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE={MYSQL_DATABASE}
MYSQL_USER={MYSQL_USER}
MYSQL_PASSWORD={MYSQL_PASSWORD}
```

Comment out below if you just want to run local: uvicorn app.main:app --reload

```bash
MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE={MYSQL_DATABASE}
MYSQL_USER={MYSQL_USER}
MYSQL_PASSWORD={MYSQL_PASSWORD}
```

### Start the service

Run docker-compose

```bash
docker-compose up --build
```

The application should now be running at `http://0.0.0.0:8000`.

```bash
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Waiting for application startup.
INFO:     Application startup complete.
...
INFO:     XXX.X.X.X:XXXX - "GET /events/ HTTP/1.1" 200 OK
```

## Usage

### Option 1

Navigate to http://0.0.0.0:8000/docs# to view the Swagger UI documentation and test the API endpoints. You can use CURL commands or link to a Postman collection if available.

Something we can do......

#### View Events

```bash
$ curl -X 'GET' \
  'http://0.0.0.0:8000/events/' \
  -H 'accept: application/json'
```

#### Add a User

```bash
$ curl -X 'POST' \
  'http://0.0.0.0:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Tom"
}'
```

#### Make a Reservation

```bash
$ curl -X 'POST' \
  'http://0.0.0.0:8000/reservations/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "event_id": 1,
  "tickets_reserved": 2
}'
```

#### Update a Reservation

```bash
$ curl -X 'PUT' \
  'http://0.0.0.0:8000/reservations/1?tickets_reserved=5' \
  -H 'accept: application/json'
```

### Option 2

I also create a user-friendly, pretty format interface for the users to test the API.

#### Run Client file

```bash
python cli.py
```

Then it will pop out an command line interface for you:

```bash
--- Event Ticketing CLI ---
1: List Events
2: Create Event
3: Delete Event
4: List Users
5: Create User
6: Delete User
7: Create Reservation
8: Update Reservation
9: Delete Reservation
10: Get User Reservations
11: Lookup Reservation
12: Exit
Enter choice:
```
