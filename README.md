# Event Ticketing Service

```bash
    ______                 __     _______      __        __  _                _____                 _
   / ____/   _____  ____  / /_   /_  __(_)____/ /_____  / /_(_)___  ____ _   / ___/___  ______   __(_)_______
  / __/ | | / / _ \/ __ \/ __/    / / / / ___/ //_/ _ \/ __/ / __ \/ __ `/   \__ \/ _ \/ ___/ | / / / ___/ _ \
 / /___ | |/ /  __/ / / / /_     / / / / /__/ ,< /  __/ /_/ / / / / /_/ /   ___/ /  __/ /   | |/ / / /__/  __/
/_____/ |___/\___/_/ /_/\__/    /_/ /_/\___/_/|_|\___/\__/_/_/ /_/\__, /   /____/\___/_/    |___/_/\___/\___/
                                                                 /____/


--- Event Ticketing CLI ---
1: List Events
2: Create Event
3: List Users
4: Create User
5: Create Reservation
6: Update Reservation
7: Delete Reservation
8: Get User Reservations
9: Lookup Reservation
10: Exit
Enter choice:
```

This project is an event ticketing service built with FastAPI and MySQL. It allows users to view events, make reservations for tickets, and manage their reservations.

## Features

- View a list of all events and associated information such as name, date, and number of tickets available.
- Make a reservation for a number of tickets for a given event.
- Manage an existing ticket reservation (change the number of tickets or cancel the reservation).
- Utilizes MySQL for data persistence.
- Dockerized application setup including a MySQL database.

## Technologies

- FastAPI
- MySQL
- Pydantic
- SQLAlchemy
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

You can see the documentation via OpenAPI: `http://0.0.0.0:8000/docs#` and use Curl or Postman to test the API.

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
3: Create User
4: Create Reservation
5: Update Reservation
6: Delete Reservation
7: Get User Reservations
8: Lookup Reservation
9: Exit
Enter choice:
```
