SkyHigh Airlines Reservation System

A comprehensive Airline Reservation and Ticket Management System built with Django. This application manages flight scheduling, seat availability, ticket booking, and user roles (Admin, Staff, Passengers) with a modern, responsive UI and an integrated AI Chatbot.

🛠️ Tech Stack

Backend: Python, Django

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

Database: SQLite (Default)

Icons: FontAwesome

AI/NLP: Custom Python-based Logic Engine (No external API keys required)

🚀 How to Run the Project

Follow these steps to get the project running on your local machine.

1. Prerequisites

Ensure you have Python installed. You can check by running:

python --version


2. Download project and extract it and move to project folder in terminal using cd command.


3. Install Dependencies

Install Django and other required packages using below command

pip install -r requirements.txt


4. Database Setup

Initialize the database and apply the models using below command.

python manage.py makemigrations
python manage.py migrate


5. Create Admin Account

Create a Superuser to access the Admin Panel.

python manage.py createsuperuser


Follow the prompts to set a username (e.g., admin), email, and password.

6. Run the Server

Start the development server.

python manage.py runserver


Open your browser and visit: http://127.0.0.1:8000/

🔄 Project Control Flow

Here is how the system works for different users:

1. Public / Guest User

Homepage: Can view the landing page, "About Us", and "Contact Us".

Search: Can search for flights by Origin, Destination, and Date.

Chatbot: Can use the AI Chatbot (bottom right) to ask about flight schedules.

Action: If they try to book a flight, they are redirected to Login/Signup.

2. Passenger (Customer)

Sign Up/Login: Creates an account or logs in.

Booking Flow:

Search for a flight.

Select a flight and click "Book Now".

Seat Selection: Choose seats on a visual plane map (Green = Available).

Passenger Details: Enter names for all selected seats.

Payment: Confirm and "Pay" (Simulated).

My Bookings: View a history of all trips.

Actions:

Download Ticket: View/Print a realistic Boarding Pass.

Cancel Booking: Cancel a trip (allowed only if flight is >5 hours away).

3. Administrator (Superuser)

Login: Uses the superuser credentials.

Dashboard: Sees high-level stats (Total Flights, Revenue, etc.).

Management:

Manage Flights: Add, Edit, or Delete flight schedules.

Manage Aircraft: Add new planes with seat configurations.

Manage Staff: Create and manage accounts for Airline Staff.

View Bookings: Search any booking by PNR and view/print tickets for customers.

4. Airline Staff

Login: Logs in with credentials provided by the Admin.

Daily Overview: Sees today's flights, delays, and check-in stats.

Operations:

Flight Status: Update status (On Time, Delayed, Boarding) and assign Gate numbers.

Passenger Manifest: View list of passengers for a specific flight.

Check-In: Physically check passengers in (toggles status) and print boarding passes.

Search: Find any passenger by Name or PNR to assist them.

🤖 AI Chatbot Features

The built-in "SkyHigh AI" can understand natural language queries without external APIs.

Flight Search:

"Show flights from Pune to Patna tomorrow"

"Flights to Delhi"

Booking Status:

"Check PNR 17D232"

"Status of booking ABC123"