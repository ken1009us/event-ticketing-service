import requests

from pyfiglet import Figlet
from validation.input_validation import validate_int, validate_datetime

API_BASE_URL = "http://0.0.0.0:8000"


def create_event():
    print("\n--- Create Event ---")
    name = input("Name: ")
    description = input("Description: ")

    date_time_str = input("Date and Time (YYYY-MM-DD HH:MM:SS): ")
    valid_date, date_time = validate_datetime(date_time_str)
    if not valid_date:
        print(date_time)
        return

    date_time_iso = date_time.isoformat()

    tickets_total_str = input("Total Tickets: ")
    valid_tickets, tickets_total = validate_int(tickets_total_str, "Total Tickets")
    if not valid_tickets:
        print(tickets_total)
        return

    event = {
        "name": name,
        "description": description,
        "date_time": date_time,
        "tickets_total": int(tickets_total),
        "tickets_available": int(tickets_total),
    }
    response = requests.post(f"{API_BASE_URL}/events/", json=event)
    if response.status_code == 201:
        print("Event created successfully.")
    else:
        print(
            f"Failed to create event.  Status code: {response.status_code}, Detail: {response.text}"
        )


def list_events():
    print("\n--- List of Events ---")
    response = requests.get(f"{API_BASE_URL}/events/")
    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(f"Event ID: {event['id']}")
            print(f"Name: {event['name']}")
            print(f"Description: {event['description']}")
            print(f"Date and Time: {event['date_time']}")
            print(f"Total Tickets: {event['tickets_total']}")
            print(f"Tickets Available: {event['tickets_available']}\n")
    else:
        print(
            f"Failed to fetch events.  Status code: {response.status_code}, Detail: {response.text}"
        )


def create_user():
    print("\n--- Create User ---")
    name = input("Name: ")
    user = {"name": name}
    response = requests.post(f"{API_BASE_URL}/users/", json=user)
    if response.status_code == 201:
        print("User created successfully.")
    else:
        print(
            f"Failed to create user.  Status code: {response.status_code}, Detail: {response.text}"
        )


def list_users():
    print("\n--- List of Users ---")
    response = requests.get(f"{API_BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(f"ID: {user['id']}, Name: {user['name']}")
    else:
        print(
            f"Failed to fetch users. Status code: {response.status_code}, Detail: {response.text}"
        )


def get_user_reservations():
    print("\n--- User Reservations ---")
    user_id = input("Enter User ID: ")
    response = requests.get(f"{API_BASE_URL}/users/{user_id}/reservations")
    if response.status_code == 200:
        reservations = response.json()
        if reservations:
            for reservation in reservations:
                print(f"Reservation ID: {reservation['id']}")
                print(f"Event ID: {reservation['event_id']}")
                print(f"Tickets Reserved: {reservation['tickets_reserved']}\n")
        else:
            print("No reservations found for this user.")
    else:
        print(
            f"Failed to fetch reservations. Status code: {response.status_code}, Detail: {response.text}"
        )


def create_reservation():
    print("\n--- Create Reservation ---")
    user_id_str = input("User ID: ")
    valid_user_id, user_id = validate_int(user_id_str, "User ID")
    if not valid_user_id:
        print(user_id)
        return

    event_id_str = input("Event ID: ")
    valid_event_id, event_id = validate_int(event_id_str, "Event ID")
    if not valid_event_id:
        print(event_id)
        return

    tickets_reserved_str = input("Tickets Reserved: ")
    valid_tickets, tickets_reserved = validate_int(
        tickets_reserved_str, "Tickets Reserved"
    )
    if not valid_tickets:
        print(tickets_reserved)
        return

    reservation = {
        "user_id": int(user_id),
        "event_id": int(event_id),
        "tickets_reserved": int(tickets_reserved),
    }
    response = requests.post(f"{API_BASE_URL}/reservations/", json=reservation)
    if response.status_code == 201:
        print("Reservation created successfully:")
        print(f"User ID: {reservation['user_id']}")
        print(f"Event ID: {reservation['event_id']}")
        print(f"Tickets Reserved: {reservation['tickets_reserved']}")
    else:
        print(
            f"Failed to create reservation.  Status code: {response.status_code}, Detail: {response.text}"
        )


def lookup_reservation():
    print("\n--- Lookup Reservation ---")
    response = requests.get(f"{API_BASE_URL}/reservations/")
    if response.status_code == 200:
        reservations = response.json()
        for index, reservation in enumerate(reservations):
            print(f"Reservation {index + 1} Details:")
            print("--------------------------------")
            print(f"Reservation ID: {reservation['id']}")
            print(f"User ID: {reservation['user_id']}")
            print(f"Event ID: {reservation['event_id']}")
            print(f"Tickets Reserved: {reservation['tickets_reserved']}\n")
    else:
        print(
            f"Failed to lookup reservation.  Status code: {response.status_code}, Detail: {response.text}"
        )


def update_reservation():
    print("\n--- Update Reservation ---")
    user_id_str = input("User ID: ")
    valid_user_id, user_id = validate_int(user_id_str, "User ID")
    if not valid_user_id:
        print(user_id)
        return

    reservation_id_str = input("Reservation ID: ")
    reservation_id_str, reservation_id = validate_int(reservation_id_str, "User ID")
    if not reservation_id_str:
        print(reservation_id)
        return

    tickets_reserved_str = input("New Tickets Reserved: ")
    valid_tickets, tickets_reserved = validate_int(
        tickets_reserved_str, "Tickets Reserved"
    )
    if not valid_tickets:
        print(tickets_reserved)
        return

    data = {"user_id": int(user_id), "tickets_reserved": int(tickets_reserved)}
    response = requests.put(f"{API_BASE_URL}/reservations/{reservation_id}", json=data)
    if response.status_code == 200:
        print("Reservation updated successfully.")
        reservation = response.json()
        print(f"Reservation ID: {reservation['id']}")
        print(f"User ID: {reservation['user_id']}")
        print(f"Event ID: {reservation['event_id']}")
        print(f"Tickets Reserved: {reservation['tickets_reserved']}")
    else:
        print(
            f"Failed to update reservation.  Status code: {response.status_code}, Detail: {response.text}"
        )


def delete_reservation():
    print("\n--- Delete Reservation ---")
    reservation_id_str = input("Reservation ID: ")
    reservation_id_str, reservation_id = validate_int(reservation_id_str, "User ID")
    if not reservation_id_str:
        print(reservation_id)
        return

    response = requests.delete(f"{API_BASE_URL}/reservations/{reservation_id}")
    if response.status_code == 204:
        print("Reservation deleted successfully.")
    else:
        print(
            f"Failed to delete reservation.  Status code: {response.status_code}, Detail: {response.text}"
        )


def main_menu():
    print("\n--- Event Ticketing CLI ---")
    print("1: List Events")
    print("2: Create Event")
    print("3: List Users")
    print("4: Create User")
    print("5: Create Reservation")
    print("6: Update Reservation")
    print("7: Delete Reservation")
    print("8: Get User Reservations")
    print("9: Lookup Reservation")
    print("10: Exit")
    choice = input("Enter choice: ")
    return choice


def main():
    while True:
        choice = main_menu()
        if choice == "1":
            list_events()
        elif choice == "2":
            create_event()
        elif choice == "3":
            list_users()
        elif choice == "4":
            create_user()
        elif choice == "5":
            create_reservation()
        elif choice == "6":
            update_reservation()
        elif choice == "7":
            delete_reservation()
        elif choice == "8":
            get_user_reservations()
        elif choice == "9":
            lookup_reservation()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    f = Figlet(font="slant")
    print(f.renderText("Event Ticketing Service"))
    main()
