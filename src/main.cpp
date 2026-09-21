#include <iostream>
#include <map>
#include <vector>
#include <algorithm>
#include <numeric>
#include <fstream>
#include <filesystem>
#include "../include/models.h"
#include "../include/services.h"
#include "../include/utils.h"
#include "../include/api.h"

std::map<int, Employee*> employees;
std::vector<Attendance> attendanceRecords;

std::vector<Payroll> payrollRecords;
Settings appSettings;
std::string currentUserRole;

void checkAdminOrHR() {
    if (currentUserRole != "ADMIN" && currentUserRole != "HR") {
        throw BaseException("Permission Denied: Requires ADMIN or HR role.");
    }
}

void initializeSampleData() {
    if(!employees.empty()) {
        std::cout << "Data already exists. Skipping sample initialization to avoid overwrite.\n";
        utils::pauseScreen();
        return;
    }
    employees[101] = new Developer(101, "Alice Smith", 28, "F", "1234567890", "alice@abc.com", "Address1", "IT", 80000, "2023-01-15");
    employees[102] = new Manager(102, "Bob Jones", 35, "M", "0987654321", "bob@abc.com", "Address2", "HR", 90000, "2022-05-10");
    employees[103] = new Employee(103, "Charlie Brown", 40, "M", "1112223333", "charlie@abc.com", "Address3", "Finance", "Analyst", 75000, "2021-11-20");
    employees[104] = new Manager(104, "Diana Prince", 30, "F", "4445556666", "diana@abc.com", "Address4", "Operations", 70000, "2020-03-01");
    employees[105] = new Developer(105, "Eve Davis", 26, "F", "7778889999", "eve@abc.com", "Address5", "IT", 82000, "2023-06-15");
    
    attendanceRecords.push_back({101, "2024-01-01", true, 2});
    attendanceRecords.push_back({102, "2024-01-01", true, 0});
    
    
    
    std::cout << "Sample data initialized successfully!\n";
    AuditLogger::log(currentUserRole, "INITIALIZE SAMPLE DATA");
    utils::pauseScreen();
}

void employeeMenu() {
    int choice;
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "             EMPLOYEE MANAGEMENT MENU\n"
                  << "====================================================\n"
                  << "1. Add Employee\n"
                  << "2. View All Employees\n"
                  << "3. Search Employee\n"
                  << "4. Update Employee\n"
                  << "5. Delete Employee\n"
                  << "6. Back\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        
        try {
            if (choice == 1) {
                checkAdminOrHR();
                int id = utils::getValidatedInput<int>("Enter ID: ");
                if (employees.find(id) != employees.end()) {
                    throw InvalidInputException("ID already exists.");
                }
                std::string name, dept, desig;
                double salary;
                std::cout << "Enter Name: "; std::getline(std::cin, name);
                dept = utils::getValidatedInput<std::string>("Enter Dept (IT/HR/Finance): ");
                desig = utils::getValidatedInput<std::string>("Enter Designation (Manager/Developer/HR/Other): ");
                salary = utils::getValidatedInput<double>("Enter Basic Salary: ");
                if (salary < 0) throw InvalidInputException("Salary cannot be negative.");
                
                Employee* e = nullptr;
                if (desig == "Manager") e = new Manager(id, name, 25, "M", "9999999999", "email@test.com", "Address", dept, salary, utils::getCurrentDate());
                else if (desig == "Developer") e = new Developer(id, name, 25, "M", "9999999999", "email@test.com", "Address", dept, salary, utils::getCurrentDate());
                else if (desig == "HR") e = new HR(id, name, 25, "M", "9999999999", "email@test.com", "Address", dept, salary, utils::getCurrentDate());
                else e = new Employee(id, name, 25, "M", "9999999999", "email@test.com", "Address", dept, desig, salary, utils::getCurrentDate());
                
                employees[id] = e;
                AuditLogger::log(currentUserRole, "ADD EMPLOYEE", id);
                std::cout << "Employee Added Successfully!\n";
                utils::pauseScreen();
            } else if (choice == 2) {
                std::cout << "\n--- All Employees ---\n";
                for (const auto& pair : employees) {
                    pair.second->displayDetails(); // Polymorphism in action
                }
                utils::pauseScreen();
            } else if (choice == 3) {
                int id = utils::getValidatedInput<int>("Enter ID to search: ");
                if (employees.find(id) == employees.end()) {
                    throw EmployeeNotFoundException(std::to_string(id));
                }
                employees[id]->displayDetails();
                utils::pauseScreen();
            } else if (choice == 4) {
                checkAdminOrHR();
                int id = utils::getValidatedInput<int>("Enter ID to update: ");
                if (employees.find(id) == employees.end()) throw EmployeeNotFoundException(std::to_string(id));
                
                double newSalary = utils::getValidatedInput<double>("Enter New Salary: ");
                if (newSalary < 0) throw InvalidInputException("Salary cannot be negative.");
                employees[id]->setBasicSalary(newSalary);
                AuditLogger::log(currentUserRole, "UPDATE EMPLOYEE", id);
                std::cout << "Employee Updated Successfully!\n";
                utils::pauseScreen();
            } else if (choice == 5) {
                if (currentUserRole != "ADMIN") throw BaseException("Permission Denied: Only ADMIN can delete.");
                int id = utils::getValidatedInput<int>("Enter ID to delete: ");
                auto it = employees.find(id);
                if (it != employees.end()) {
                    delete it->second;
                    employees.erase(it);
                    AuditLogger::log(currentUserRole, "DELETE EMPLOYEE", id);
                    std::cout << "Employee Deleted.\n";
                } else {
                    throw EmployeeNotFoundException(std::to_string(id));
                }
                utils::pauseScreen();
            }
        } catch (const BaseException& e) {
            std::cout << "Error: " << e.what() << "\n";
            utils::pauseScreen();
        }
    } while (choice != 6);
}

void attendanceMenu() {
    int choice;
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "             ATTENDANCE MANAGEMENT MENU\n"
                  << "====================================================\n"
                  << "1. Mark Attendance\n"
                  << "2. View All Attendance\n"
                  << "3. Back\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        try {
            if (choice == 1) {
                checkAdminOrHR();
                int id = utils::getValidatedInput<int>("Enter Employee ID: ");
                if(employees.find(id) == employees.end()) throw EmployeeNotFoundException(std::to_string(id));
                std::string date = utils::getValidatedInput<std::string>("Enter Date (YYYY-MM-DD): ");
                int ot = utils::getValidatedInput<int>("Enter Overtime Hours (0 if none): ");
                attendanceRecords.push_back({id, date, true, ot});
                AuditLogger::log(currentUserRole, "MARK ATTENDANCE", id);
                std::cout << "Attendance Marked!\n";
                utils::pauseScreen();
            } else if (choice == 2) {
                std::cout << "\n--- Attendance Records ---\n";
                for (const auto& a : attendanceRecords) {
                    std::cout << "EmpID: " << a.employeeId << " | Date: " << a.date << " | Present: " << (a.isPresent ? "Yes" : "No") << " | OT: " << a.overtimeHours << " hrs\n";
                }
                utils::pauseScreen();
            }
        } catch (const BaseException& e) {
            std::cout << "Error: " << e.what() << "\n";
            utils::pauseScreen();
        }
    } while(choice != 3);
}

void payrollMenu() {
    int choice;
    PayrollManager pm(appSettings);
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "             PAYROLL MANAGEMENT MENU\n"
                  << "====================================================\n"
                  << "1. Generate Employee Payroll\n"
                  << "2. View Payroll History\n"
                  << "3. Mark Payroll as Paid\n"
                  << "4. Back\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        
        try {
            if (choice == 1) {
                checkAdminOrHR();
                int id = utils::getValidatedInput<int>("Enter Employee ID: ");
                if (employees.find(id) == employees.end()) {
                    throw EmployeeNotFoundException(std::to_string(id));
                }
                std::string month = utils::getValidatedInput<std::string>("Enter Month (e.g. Jan-2023): ");
                int ot = utils::getValidatedInput<int>("Enter OT Hours: ");
                double bonus = utils::getValidatedInput<double>("Enter Bonus: ");
                
                auto it = std::find_if(payrollRecords.begin(), payrollRecords.end(), [&](const Payroll& p){
                    return p.employeeId == id && p.month == month;
                });
                if(it != payrollRecords.end()) throw BaseException("Payroll for this month already exists!");
                
                Payroll p = pm.calculatePayroll(*employees[id], month, ot, bonus, 0.0);
                payrollRecords.push_back(p);
                pm.generateSalarySlip(*employees[id], p);
                AuditLogger::log(currentUserRole, "GENERATE PAYROLL", id);
                std::cout << "Payroll Generated Successfully!\n";
                utils::pauseScreen();
            } else if (choice == 2) {
                std::cout << "\n--- Payroll History ---\n";
                for (size_t i=0; i<payrollRecords.size(); i++) {
                    const auto& p = payrollRecords[i];
                    std::cout << "[" << i << "] EmpID: " << p.employeeId << " | Month: " << p.month << " | Net: " << p.netSalary << " | Paid: " << (p.isPaid ? "Yes" : "No") << "\n";
                }
                utils::pauseScreen();
            } else if (choice == 3) {
                checkAdminOrHR();
                int idx = utils::getValidatedInput<int>("Enter Payroll Index: ");
                if (idx < 0 || idx >= (int)payrollRecords.size()) throw InvalidInputException("Invalid Index");
                payrollRecords[idx].isPaid = true;
                AuditLogger::log(currentUserRole, "PAYROLL PAID", payrollRecords[idx].employeeId);
                std::cout << "Payroll Marked as Paid!\n";
                utils::pauseScreen();
            }
        } catch (const BaseException& e) {
            std::cout << "Error: " << e.what() << "\n";
            utils::pauseScreen();
        }
    } while (choice != 4);
}

void reportMenu() {
    int choice;
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "             REPORT MENU\n"
                  << "====================================================\n"
                  << "1. Employee Summary\n"
                  << "2. Department Distribution\n"
                  << "3. Attendance Summary\n"
                  << "4. Payroll Summary\n"
                  << "5. Filter by Department (Function Overloading)\n"
                  << "6. Search Active Employees (STL algorithm)\n"
                  << "7. View Audit Log\n"
                  << "8. Back\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        
        if (choice == 1) {
            ReportManager::generateEmployeeReport(employees);
            utils::pauseScreen();
        } else if (choice == 2) {
            ReportManager::generateDepartmentReport(employees);
            utils::pauseScreen();
        } else if (choice == 3) {
            ReportManager::generateAttendanceReport(attendanceRecords);
            utils::pauseScreen();
        } else if (choice == 4) {
            ReportManager::generatePayrollReport(payrollRecords);
            utils::pauseScreen();
        } else if (choice == 5) {
            std::string dept = utils::getValidatedInput<std::string>("Enter Department: ");
            ReportManager::generateEmployeeReport(employees, dept); // Function overloading
            utils::pauseScreen();
        } else if (choice == 6) {
            std::cout << "\n--- Active Employees ---\n";
            // Demo STL algorithm
            std::for_each(employees.begin(), employees.end(), [](const std::pair<int, Employee*>& p) {
                if (p.second->getStatus() == EmploymentStatus::ACTIVE) {
                    p.second->displayDetails();
                }
            });
            utils::pauseScreen();
        } else if (choice == 7) {
            std::cout << "\n--- Audit Log ---\n";
            std::ifstream in("data/audit.log");
            if (in) {
                std::string line;
                while (std::getline(in, line)) {
                    std::cout << line << "\n";
                }
            } else {
                std::cout << "No audit log found.\n";
            }
            utils::pauseScreen();
        }
    } while(choice != 8);
}

void settingsMenu() {
    int choice;
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "             SETTINGS MENU\n"
                  << "====================================================\n"
                  << "1. View Settings\n"
                  << "2. Update Settings\n"
                  << "3. Back\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        try {
            if(choice == 1) {
                std::cout << "\n--- Current Settings ---\n";
                std::cout << "HRA %: " << appSettings.hraPercent * 100 << "%\n";
                std::cout << "DA %: " << appSettings.daPercent * 100 << "%\n";
                std::cout << "PF %: " << appSettings.pfPercent * 100 << "%\n";
                std::cout << "Tax %: " << appSettings.taxPercent * 100 << "%\n";
                std::cout << "OT Rate: " << appSettings.overtimeRate << "\n";
                utils::pauseScreen();
            } else if (choice == 2) {
                if(currentUserRole != "ADMIN") throw BaseException("Only ADMIN can modify settings.");
                appSettings.hraPercent = utils::getValidatedInput<double>("Enter HRA % (e.g. 20): ") / 100.0;
                appSettings.daPercent = utils::getValidatedInput<double>("Enter DA % (e.g. 10): ") / 100.0;
                appSettings.pfPercent = utils::getValidatedInput<double>("Enter PF % (e.g. 12): ") / 100.0;
                appSettings.taxPercent = utils::getValidatedInput<double>("Enter Tax % (e.g. 5): ") / 100.0;
                appSettings.overtimeRate = utils::getValidatedInput<double>("Enter OT Rate: ");
                std::cout << "Settings Updated!\n";
                AuditLogger::log(currentUserRole, "UPDATE SETTINGS");
                utils::pauseScreen();
            }
        } catch (const BaseException& e) {
            std::cout << "Error: " << e.what() << "\n";
            utils::pauseScreen();
        }
    } while(choice != 3);
}

void dashboard() {
    int choice;
    do {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "           EMPLOYEE PAYROLL MANAGEMENT SYSTEM\n"
                  << "====================================================\n"
                  << "Logged in as: " << currentUserRole << "\n"
                  << "Total Employees: " << employees.size() << "\n"
                  << "Total Payrolls : " << payrollRecords.size() << "\n"
                  << "====================================================\n"
                  << "1. Employee Management\n"
                  << "2. Attendance Management\n"
                  << "3. Leave Management\n"
                  << "4. Payroll Management\n"
                  << "5. Reports & Analytics\n"
                  << "6. Settings\n"
                  << "7. Initialize Sample Data\n"
                  << "8. Save All Data\n"
                  << "9. Logout\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        
        if (choice == 1) employeeMenu();
        else if (choice == 2) attendanceMenu();
        
        else if (choice == 4) payrollMenu();
        else if (choice == 5) reportMenu();
        else if (choice == 6) settingsMenu();
        else if (choice == 7) initializeSampleData();
        else if (choice == 8) {
            FileManager::saveEmployees(employees);
            FileManager::saveAttendance(attendanceRecords);
            
            FileManager::savePayroll(payrollRecords);
            FileManager::saveSettings(appSettings);
            std::cout << "Data Saved Successfully.\n";
            utils::pauseScreen();
        }
    } while (choice != 9);
}

int main(int argc, char* argv[]) {
    std::filesystem::create_directories("data");
    std::filesystem::create_directories("salary_slips");
    
    FileManager::loadEmployees(employees);
    FileManager::loadAttendance(attendanceRecords);
    
    FileManager::loadPayroll(payrollRecords);
    FileManager::loadSettings(appSettings);
    
    std::map<std::string, User> appUsers;
    FileManager::loadUsers(appUsers);
    
    if (argc > 1 && std::string(argv[1]) == "--server") {
        startApiServer(8080, appUsers);
        return 0;
    }
    
    Authentication auth(appUsers);
    while (true) {
        try {
            currentUserRole = auth.loginScreen();
            dashboard();
            AuditLogger::log(currentUserRole, "LOGOUT");
        } catch (const AuthenticationException& e) {
            std::cout << e.what() << "\n";
            utils::pauseScreen();
        }
    }
    
    // Memory cleanup
    for(auto& p : employees) {
        delete p.second;
    }
    employees.clear();
    
    return 0;
}
