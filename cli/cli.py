import requests

from validation.input_validation import validate_int, validate_datetime

API_BASE_URL = "http://localhost:8000"


def create_event():
    print("\n--- Create Event ---")
    name = input("Name: ")
    description = input("Description: ")

    date_time_str = input("Date and Time (YYYY-MM-DD HH:MM:SS): ")
    valid_date, date_time = validate_datetime(date_time_str)
    if not valid_date:
        print(date_time)
        return

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
        print("Failed to create event.")


def list_events():
    print("\n--- List of Events ---")
    response = requests.get(f"{API_BASE_URL}/events/")
    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(f"Name: {event['name']}")
            print(f"Description: {event['description']}")
            print(f"Date and Time: {event['date_time']}")
            print(f"Total Tickets: {event['tickets_total']}")
            print(f"Tickets Available: {event['tickets_available']}\n")
    else:
        print("Failed to fetch events.")


def create_user():
    print("\n--- Create User ---")
    name = input("Name: ")
    user = {"name": name}
    response = requests.post(f"{API_BASE_URL}/users/", json=user)
    if response.status_code == 200:
        print("User created successfully.")
    else:
        print("Failed to create user.")


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
    if response.status_code == 200:
        reservation = response.json()["reservation"]
        print("Reservation created successfully:")
        print(f"User ID: {reservation['user_id']}")
        print(f"Event ID: {reservation['event_id']}")
        print(f"Tickets Reserved: {reservation['tickets_reserved']}")
    else:
        print("Failed to create reservation.")


def lookup_reservation():
    print("\n--- Lookup Reservation ---")
    response = requests.get(f"{API_BASE_URL}/reservations/")
    if response.status_code == 200:
        reservation = response.json()
        print("Reservation Details:")
        print(f"Reservation ID: {reservation['id']}")
        print(f"User ID: {reservation['user_id']}")
        print(f"Event ID: {reservation['event_id']}")
        print(f"Tickets Reserved: {reservation['tickets_reserved']}")
    else:
        print(f"Failed to lookup reservation. Detail: {response.text}")


def update_reservation():
    print("\n--- Update Reservation ---")
    reservation_id = input("Reservation ID: ")
    user_id = input("User ID: ")
    tickets_reserved = input("New Tickets Reserved: ")
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
        print(f"Failed to update reservation. Detail: {response.text}")


def delete_reservation():
    print("\n--- Delete Reservation ---")
    reservation_id = input("Reservation ID: ")
    response = requests.delete(f"{API_BASE_URL}/reservations/{reservation_id}")
    if response.status_code == 204:
        print("Reservation deleted successfully.")
    else:
        print(f"Failed to delete reservation. Detail: {response.text}")


def main_menu():
    print("\n--- Event Ticketing CLI ---")
    print("1: List Events")
    print("2: Create Event")
    print("3: Create User")
    print("4: Create Reservation")
    print("5: Update Reservation")
    print("6: Delete Reservation")
    print("7: Get User Reservations")
    print("8: Lookup Reservation")
    print("9: Exit")
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
            create_user()
        elif choice == "4":
            create_reservation()
        elif choice == "5":
            update_reservation()
        elif choice == "6":
            delete_reservation()
        elif choice == "7":
            get_user_reservations()
        elif choice == "8":
            lookup_reservation()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
