# Employee Payroll Management System

A COMPLETE, PROFESSIONAL, ADVANCED C++ console-based project.

## Objectives
Develop an Employee Payroll Management System that manages employees, payrolls, reporting, and file persistence using standard C++ concepts.

## Features
- Complete Employee Management (Add, View, Delete, Search)
- Payroll Generation (Calculate gross, net, deductions based on configurable rates)
- Salary Slips (Generate and save text-based salary slips)
- Reports & Analytics (Department distribution, Employee summary)
- Role-based Access (Admin, HR, Manager logins)
- Audit Logging (Track all operations)
- Persistent Storage (Uses File Handling to store data across restarts)
- Robust Error Handling and Input Validation

## Technologies Used
- C++17 (Standard C++)
- STL (Standard Template Library)
- Console I/O

## How to Compile
You need a standard C++ compiler (like g++, MinGW, or GCC).
For Linux/Mac:
`make` or `g++ -std=c++17 src/*.cpp -o PayrollSystem`

For Windows:
Run the provided `compile.bat` script or use:
`g++ -std=c++17 src\main.cpp src\models.cpp src\services.cpp src\utils.cpp -o bin\PayrollSystem.exe`

## How to Run
Navigate to the root directory after compiling, and execute:
Linux/Mac: `./bin/PayrollSystem`
Windows: `bin\PayrollSystem.exe`

## Default Login Credentials
Username: <your-admin-username>
Password: <your-admin-password>

## Web Frontend Integration
A modern React + Vite frontend has been added, communicating directly with the C++ backend via a REST API.

### Prerequisites
- C++ Compiler (MinGW/MSYS2) with Winsock2 (`-lws2_32`)
- Node.js (for the React frontend)

### Starting the Backend API
1. Run `BUILD.bat` to compile the C++ application (now equipped with the API server).
2. Run `RUN_SERVER.bat` to start the backend on `http://localhost:8080`.

### Starting the Frontend
1. Open a new terminal.
2. Navigate to the `frontend` directory: `cd frontend`
3. Install dependencies (if not done): `npm install`
4. Start the Vite dev server: `npm run dev`
5. Open your browser to the URL provided by Vite (e.g., `http://localhost:5173`).

## Known Limitations
- Pure console application, no GUI.
- **This authentication mechanism is designed for academic demonstration and is not intended for production security.** Passwords are stored in a simple format and standard C++ cannot portably suppress console output during password entry.
- Uses file I/O instead of a relational database.

## Future Enhancements
- Database integration (SQL)
- GUI implementation (Qt)
- Send salary slips via email
