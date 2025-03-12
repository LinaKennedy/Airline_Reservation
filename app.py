import streamlit as st

# Initialize flight data if not already present in session_state


if "flights" not in st.session_state:
    st.session_state.flights = {
        "101": {"departure": "Delhi", "destination": "Mumbai", "time": "08:30 AM", "seats": 5, "flight_number": "AI 2021"},
        "102": {"departure": "Mumbai", "destination": "Bangalore", "time": "12:45 PM", "seats": 120, "flight_number": "AI 3050"},
        "103": {"departure": "Bangalore", "destination": "Delhi", "time": "05:00 PM", "seats": 180, "flight_number": "AI 1014"},
        "104": {"departure": "Delhi", "destination": "Kolkata", "time": "10:30 AM", "seats": 100, "flight_number": "AI 2025"},
        "105": {"departure": "Kolkata", "destination": "Chennai", "time": "03:00 PM", "seats": 80, "flight_number": "AI 1503"}
    }

# Initialize reservation data if not already present in session_state
if "reservations" not in st.session_state:
    st.session_state.reservations = []

def main():
    st.title("Airline Reservation System")

    # Sidebar with radio buttons for navigation
    menu = ["View Flights", "Search Flights", "Book Tickets", "View Reservations"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "View Flights":
        view_flights()
    elif choice == "Search Flights":
        search_flights()
    elif choice == "Book Tickets":
        book_tickets()
    elif choice == "View Reservations":
        view_reservations()

def view_flights():
    st.subheader("Available Flights")
    flights = st.session_state.flights
    flight_data = [
        {
            "Flight ID": flight_id,
            "Departure": details["departure"],
            "Destination": details["destination"],
            "Time": details["time"],
            "Seats Available": details["seats"],
            "Flight Number": details["flight_number"]
        }
        for flight_id, details in flights.items()
    ]
    st.table(flight_data)

def search_flights():
    st.subheader("Search for a Flight")
    with st.form("search_form"):
        departure = st.text_input("Enter departure city")
        destination = st.text_input("Enter destination city")
        submit_button = st.form_submit_button("Search")

    if submit_button:
        found_flights = [
            {
                "Flight ID": flight_id,
                "Departure": details["departure"],
                "Destination": details["destination"],
                "Time": details["time"],
                "Seats Available": details["seats"],
                "Flight Number": details["flight_number"]
            }
            for flight_id, details in st.session_state.flights.items()
            if details["departure"].lower() == departure.lower() and details["destination"].lower() == destination.lower()
        ]
        if found_flights:
            st.table(found_flights)
        else:
            st.warning("No flights found for the specified route.")

def book_tickets():
    st.subheader("Book Tickets")
    flight_id = st.text_input("Enter Flight ID")
    num_seats = st.number_input("Enter number of seats to book", min_value=1, step=1)
    if st.button("Book"):
        if flight_id in st.session_state.flights:
            flight = st.session_state.flights[flight_id]
            if flight["seats"] >= num_seats:
                flight["seats"] -= num_seats
                st.session_state.reservations.append({"flight_id": flight_id, "seats": num_seats})
                st.success(f"Successfully booked {num_seats} seat(s) on flight {flight_id}!")
            else:
                st.error("Not enough seats available.")
        else:
            st.error("Invalid Flight ID.")

def view_reservations():
    st.subheader("Your Reservations")
    reservations = st.session_state.reservations
    if reservations:
        reservation_data = [
            {"Flight ID": res["flight_id"], "Seats Booked": res["seats"]}
            for res in reservations
        ]
        st.table(reservation_data)
    else:
        st.info("No reservations made yet.")

if __name__ == "__main__":
    main()
