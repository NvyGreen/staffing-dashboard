# Staffing Dashboard
This project is a demo dashboard built for a staffing and workforce management company. The application is designed to streamline day-to-day operations by providing managers with a centralized interface to manage clients, job requests, employees, and financial workflows.

The goal of this project is to demonstrate how a single, intuitive system can support the full staffing lifecycle—from client intake and employee assignment to invoicing and payment tracking—while improving visibility and operational efficiency.

This repository serves as a functional prototype and proof of concept rather than a production-ready system.


## Tech Stack
Frontend: HTML/CSS  
Backend: Python (Flask)  
Database: SQLite  


## Features
Through this platform, managers can:
* View and manage client accounts and incoming job requests
* Assign employees to open positions and track job placements
* Monitor invoices, payments, and outstanding balances


## Running Locally
To run this project locally:
1. Ensure Python (3.9+) and SQLite are installed on your machine.
2. Clone the repository and navigate to the project directory.
3. Create and activate a virtual environment, then install the required dependencies.
4. Create .env and .flaskenv files in the root directory to store environment variables such as the Flask configuration, secret key, and database connection details.
5. .env.example and .flaskenv.example files are provided to show the required environment variables and expected format.
6. Start the Flask development server.
7. Open the application in your browser at http://127.0.0.1:5000.
8. You should now be able to use the dashboard locally to manage clients, jobs, candidates, placements, and invoices.

### Database Setup
- The application uses a relational database with tables representing clients, job postings, candidates, placements, and invoices.
- Create a SQLite database for the application.
- Database tables are created manually during development.
- A formal schema or migration setup is planned as a future improvement.


## Future Improvements
* Implement employee payment processing and payroll functionality
* Add role-based access control for different user types
* Improve UI/UX and error handling
