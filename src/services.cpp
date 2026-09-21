#include "../include/services.h"
#include "../include/utils.h"
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <iostream>
#include <stdexcept>

inline double safeParseDouble(const std::string& str, double defaultVal = 0.0) {
    if (str.empty()) return defaultVal;
    try {
        return std::stod(str);
    } catch (const std::out_of_range&) {
        std::cerr << "\n[DATA ERROR] std::out_of_range parsing double from: " << str << "\n";
        if (str.find("e-") != std::string::npos || str.find("E-") != std::string::npos) {
            return 0.0; 
        }
        return defaultVal;
    } catch (const std::invalid_argument&) {
        std::cerr << "\n[DATA ERROR] std::invalid_argument parsing double from: " << str << "\n";
        return defaultVal;
    } catch (...) {
        std::cerr << "\n[DATA ERROR] Unknown error parsing double from: " << str << "\n";
        return defaultVal;
    }
}


void AuditLogger::log(const std::string& username, const std::string& action, int empId) {
    std::ofstream out("data/audit.log", std::ios::app);
    if (out.is_open()) {
        out << utils::getCurrentDate() << " | User: " << username << " | Action: " << action;
        if (empId != -1) out << " | EmpID: " << empId;
        out << "\n";
        out.close();
    }
}

void FileManager::saveEmployees(const std::map<int, Employee*>& employees) {
    std::ofstream out("data/employees.dat");
    if (!out) return;
    for (const auto& pair : employees) {
        const Employee* e = pair.second;
        out << e->getId() << "," << e->getName() << "," << e->getDepartment() << ","
            << e->getDesignation() << "," << e->getBasicSalary() << "," 
            << static_cast<int>(e->getStatus()) << "\n";
    }
    out.close();
}

void FileManager::loadEmployees(std::map<int, Employee*>& employees) {
    std::ifstream in("data/employees.dat");
    if (!in) return;
    std::string line;
    while (std::getline(in, line)) {
        std::stringstream ss(line);
        std::string idStr, name, dept, desig, salaryStr, statusStr;
        std::getline(ss, idStr, ',');
        std::getline(ss, name, ',');
        std::getline(ss, dept, ',');
        std::getline(ss, desig, ',');
        std::getline(ss, salaryStr, ',');
        std::getline(ss, statusStr, ',');
        if(idStr.empty()) continue;
        int id = std::stoi(idStr);
        double salary = safeParseDouble(salaryStr);
        
        Employee* e = nullptr;
        if (desig == "Manager") e = new Manager(id, name, 30, "M", "000", "e@e.com", "addr", dept, salary, "2020-01-01");
        else if (desig == "Developer") e = new Developer(id, name, 30, "M", "000", "e@e.com", "addr", dept, salary, "2020-01-01");
        else if (desig == "HR") e = new HR(id, name, 30, "M", "000", "e@e.com", "addr", dept, salary, "2020-01-01");
        else e = new Employee(id, name, 30, "M", "000", "e@e.com", "addr", dept, desig, salary, "2020-01-01");
        
        e->setStatus(static_cast<EmploymentStatus>(std::stoi(statusStr)));
        employees[id] = e;
    }
    in.close();
}

void FileManager::saveAttendance(const std::vector<Attendance>& attendance) {
    std::ofstream out("data/attendance.dat");
    for (const auto& a : attendance) {
        out << a.employeeId << "," << a.date << "," << a.isPresent << "," << a.overtimeHours << "\n";
    }
}

void FileManager::loadAttendance(std::vector<Attendance>& attendance) {
    std::ifstream in("data/attendance.dat");
    if (!in) return;
    std::string line;
    while(std::getline(in, line)) {
        std::stringstream ss(line);
        std::string idStr, date, pres, ot;
        std::getline(ss, idStr, ',');
        std::getline(ss, date, ',');
        std::getline(ss, pres, ',');
        std::getline(ss, ot, ',');
        if(idStr.empty()) continue;
        Attendance a = {std::stoi(idStr), date, pres=="1", std::stoi(ot)};
        attendance.push_back(a);
    }
}

void FileManager::savePayroll(const std::vector<Payroll>& payroll) {
    std::ofstream out("data/payroll.dat");
    for (const auto& p : payroll) {
        out << p.employeeId << "," << p.month << "," << p.basic << "," << p.hra << "," << p.da << "," << p.allowances << "," << p.bonus << "," << p.overtimePay << "," << p.pf << "," << p.tax << "," << p.deductions << "," << p.netSalary << "," << p.isPaid << "\n";
    }
}

void FileManager::loadPayroll(std::vector<Payroll>& payroll) {
    std::ifstream in("data/payroll.dat");
    if(!in) return;
    std::string line;
    while(std::getline(in, line)) {
        std::stringstream ss(line);
        std::string id, month, basic, hra, da, allow, bonus, ot, pf, tax, ded, net, paid;
        std::getline(ss, id, ',');
        std::getline(ss, month, ',');
        std::getline(ss, basic, ',');
        std::getline(ss, hra, ',');
        std::getline(ss, da, ',');
        std::getline(ss, allow, ',');
        std::getline(ss, bonus, ',');
        std::getline(ss, ot, ',');
        std::getline(ss, pf, ',');
        std::getline(ss, tax, ',');
        std::getline(ss, ded, ',');
        std::getline(ss, net, ',');
        std::getline(ss, paid, ',');
        if(id.empty()) continue;
        Payroll p;
        p.employeeId = std::stoi(id);
        p.month = month;
        p.basic = safeParseDouble(basic);
        p.hra = safeParseDouble(hra);
        p.da = safeParseDouble(da);
        p.allowances = safeParseDouble(allow);
        p.bonus = safeParseDouble(bonus);
        p.overtimePay = safeParseDouble(ot);
        p.pf = safeParseDouble(pf);
        p.tax = safeParseDouble(tax);
        p.deductions = safeParseDouble(ded);
        p.netSalary = safeParseDouble(net);
        p.isPaid = (paid == "1");
        payroll.push_back(p);
    }
}

void FileManager::saveSettings(const Settings& settings) {
    std::ofstream out("data/settings.dat");
    if(out.is_open()) {
        out << settings.hraPercent << "," << settings.daPercent << "," << settings.pfPercent << "," << settings.taxPercent << "," << settings.overtimeRate << "\n";
        out.close();
    }
}

void FileManager::loadSettings(Settings& settings) {
    std::ifstream in("data/settings.dat");
    if(!in) return;
    std::string line;
    if(std::getline(in, line)) {
        std::stringstream ss(line);
        std::string h, d, p, t, o;
        std::getline(ss, h, ',');
        std::getline(ss, d, ',');
        std::getline(ss, p, ',');
        std::getline(ss, t, ',');
        std::getline(ss, o, ',');
        if(!h.empty()) {
            settings.hraPercent = safeParseDouble(h);
            settings.daPercent = safeParseDouble(d);
            settings.pfPercent = safeParseDouble(p);
            settings.taxPercent = safeParseDouble(t);
            settings.overtimeRate = safeParseDouble(o);
        }
    }
}

Payroll PayrollManager::calculatePayroll(const Employee& emp, const std::string& month, int otHours, double bonus, double otherDeductions) {
    Payroll p;
    p.employeeId = emp.getId();
    p.month = month;
    p.basic = emp.getBasicSalary();
    p.hra = p.basic * settings.hraPercent;
    p.da = p.basic * settings.daPercent;
    p.allowances = 0;
    p.bonus = bonus;
    p.overtimePay = otHours * settings.overtimeRate;
    
    double gross = p.basic + p.hra + p.da + p.allowances + p.bonus + p.overtimePay;
    
    p.pf = p.basic * settings.pfPercent;
    p.tax = gross * settings.taxPercent;
    p.deductions = otherDeductions + p.pf + p.tax;
    
    p.netSalary = gross - p.deductions;
    p.isPaid = false;
    
    return p;
}

void PayrollManager::generateSalarySlip(const Employee& emp, const Payroll& p) {
    std::string filename = "salary_slips/Slip_" + std::to_string(emp.getId()) + "_" + p.month + ".txt";
    std::ofstream out(filename);
    if (!out) {
        std::cerr << "Failed to generate salary slip.\n";
        return;
    }
    
    out << "================================================\n"
        << "             EMPLOYEE PAYROLL SYSTEM\n"
        << "                  SALARY SLIP\n"
        << "================================================\n\n"
        << "Employee ID: " << emp.getId() << "\n"
        << "Employee Name: " << emp.getName() << "\n"
        << "Department: " << emp.getDepartment() << "\n"
        << "Designation: " << emp.getDesignation() << "\n"
        << "Month: " << p.month << "\n\n"
        << "---------------- EARNINGS ----------------\n"
        << "Basic Salary: " << p.basic << "\n"
        << "HRA: " << p.hra << "\n"
        << "DA: " << p.da << "\n"
        << "Overtime: " << p.overtimePay << "\n"
        << "Bonus: " << p.bonus << "\n"
        << "Gross Salary: " << (p.basic + p.hra + p.da + p.allowances + p.bonus + p.overtimePay) << "\n\n"
        << "--------------- DEDUCTIONS ----------------\n"
        << "PF: " << p.pf << "\n"
        << "Income Tax: " << p.tax << "\n"
        << "Other Deductions: " << (p.deductions - p.pf - p.tax) << "\n"
        << "Total Deductions: " << p.deductions << "\n\n"
        << "--------------- NET SALARY ----------------\n"
        << "Net Salary: " << p.netSalary << "\n\n"
        << "Payment Status: " << (p.isPaid ? "PAID" : "PENDING") << "\n"
        << "================================================\n";
    out.close();
    std::cout << "Salary slip generated at: " << filename << std::endl;
}

void ReportManager::generateEmployeeReport(const std::map<int, Employee*>& employees) {
    std::cout << "\n--- Employee Report ---\n";
    std::cout << "Total Employees: " << employees.size() << "\n";
    int active = 0;
    for (const auto& pair : employees) {
        if (pair.second->getStatus() == EmploymentStatus::ACTIVE) active++;
    }
    std::cout << "Active: " << active << " | Inactive: " << employees.size() - active << "\n";
}

void ReportManager::generateEmployeeReport(const std::map<int, Employee*>& employees, const std::string& deptFilter) {
    std::cout << "\n--- Employee Report (" << deptFilter << ") ---\n";
    int count = 0;
    for (const auto& pair : employees) {
        if (pair.second->getDepartment() == deptFilter) {
            pair.second->displayDetails();
            count++;
        }
    }
    std::cout << "Total in " << deptFilter << ": " << count << "\n";
}

void ReportManager::generateDepartmentReport(const std::map<int, Employee*>& employees) {
    std::map<std::string, int> deptCount;
    for (const auto& pair : employees) {
        deptCount[pair.second->getDepartment()]++;
    }
    std::cout << "\n--- Department Report ---\n";
    for (const auto& pair : deptCount) {
        std::cout << std::left << std::setw(10) << pair.first << " : ";
        for (int i=0; i<pair.second; i++) std::cout << "#";
        std::cout << " " << pair.second << "\n";
    }
}

void ReportManager::generateAttendanceReport(const std::vector<Attendance>& attendance) {
    std::cout << "\n--- Attendance Report ---\n";
    std::cout << "Total Attendance Records: " << attendance.size() << "\n";
    int present = 0, overtime = 0;
    for(const auto& a : attendance) {
        if(a.isPresent) present++;
        overtime += a.overtimeHours;
    }
    std::cout << "Total Present Days: " << present << "\n";
    std::cout << "Total Overtime Hours: " << overtime << "\n";
}

void ReportManager::generatePayrollReport(const std::vector<Payroll>& payrolls) {
    std::cout << "\n--- Payroll Report ---\n";
    std::cout << "Total Payroll Records: " << payrolls.size() << "\n";
    double totalNet = 0;
    for(const auto& p : payrolls) {
        totalNet += p.netSalary;
    }
    std::cout << "Total Payout: Rs. " << std::fixed << std::setprecision(2) << totalNet << "\n";
}

void FileManager::saveUsers(const std::map<std::string, User>& users) {
    std::ofstream out("data/users.dat");
    for (const auto& pair : users) {
        out << pair.second.username << "," << pair.second.password << ","
            << pair.second.role << "," << pair.second.securityQuestion << ","
            << pair.second.securityAnswer << "\n";
    }
}

void FileManager::loadUsers(std::map<std::string, User>& users) {
    std::ifstream in("data/users.dat");
    if (!in) {
        // Initialize default users if file doesn't exist
        users["admin"] = {"admin", "admin123", "ADMIN", "What is your employee ID?", "1"};
        users["hr"] = {"hr", "hr123", "HR", "What is your employee ID?", "2"};
        users["manager"] = {"manager", "manager123", "MANAGER", "What is your employee ID?", "3"};
        return;
    }
    std::string line;
    while(std::getline(in, line)) {
        std::stringstream ss(line);
        std::string u, p, r, sq, sa;
        std::getline(ss, u, ',');
        std::getline(ss, p, ',');
        std::getline(ss, r, ',');
        std::getline(ss, sq, ',');
        std::getline(ss, sa, ',');
        if (!u.empty()) {
            users[u] = {u, p, r, sq, sa};
        }
    }
}

std::string Authentication::getHiddenPassword() {
    std::string pass = "";
    // Note: Standard C++ does not have a portable way to hide password input natively without echoing.
    // For academic purposes and to remain strictly portable C++17, we simply read the string.
    // Platform-specific <conio.h> (_getch) or termios is omitted to strictly satisfy "portable standard C++17" constraints.
    // We document this limitation as requested.
    std::cin >> pass;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return pass;
}

std::string Authentication::normalLogin() {
    std::string pass;
    std::string user = utils::getValidatedInput<std::string>("Username / Email: ");
    std::cout << "Password: ";
    pass = getHiddenPassword();
    
    if (user.empty() || pass.empty()) {
        AuditLogger::log("UNKNOWN", "LOGIN_FAILED");
        throw AuthenticationException("Username or password cannot be empty.");
    }
    
    auto it = users.find(user);
    if (it != users.end() && it->second.password == pass) {
        AuditLogger::log(user, "LOGIN_SUCCESS");
        return it->second.role;
    }
    
    AuditLogger::log(user, "LOGIN_FAILED");
    throw AuthenticationException("Invalid credentials!");
}

std::string Authentication::googleDemoLogin() {
    std::cout << "\n----------------------------------------------------\n";
    std::cout << "             GOOGLE SIGN-IN DEMO\n";
    std::cout << "----------------------------------------------------\n";
    std::cout << "Google account:\n";
    std::cout << "demo.google@example.com\n\n";
    std::cout << "[Continue] (Press Enter)\n";
    std::cin.ignore();
    std::cin.get();
    
    std::cout << "Demo Google authentication successful.\n";
    std::cout << "DEMO / SIMULATED GOOGLE SIGN-IN\n";
    AuditLogger::log("demo.google@example.com", "GOOGLE_DEMO_LOGIN");
    
    utils::pauseScreen();
    // Map demo to HR role
    return "HR"; 
}

void Authentication::forgotPassword() {
    std::cout << "\n====================================================\n";
    std::cout << "                 RESET PASSWORD\n";
    std::cout << "====================================================\n";
    
    std::string user = utils::getValidatedInput<std::string>("Enter registered username/email: ");
    
    auto it = users.find(user);
    if (it == users.end()) {
        std::cout << "Account not found.\n";
        utils::pauseScreen();
        return;
    }
    
    std::cout << "Security Question: \n" << it->second.securityQuestion << "\nAnswer: ";
    std::string ans;
    std::getline(std::cin, ans);
    
    if (ans == it->second.securityAnswer) {
        std::string p1 = utils::getValidatedInput<std::string>("Enter New Password: ");
        std::string p2 = utils::getValidatedInput<std::string>("Confirm New Password: ");
        
        if (p1.empty() || p1.length() < 5) {
            std::cout << "Password too short! Minimum 5 characters.\n";
        } else if (p1 == p2) {
            it->second.password = p1; // Simple storage
            FileManager::saveUsers(users); // Persist immediately
            AuditLogger::log(user, "PASSWORD_RESET");
            std::cout << "Password reset successful.\n";
        } else {
            std::cout << "Passwords do not match!\n";
        }
    } else {
        std::cout << "Incorrect answer!\n";
    }
    utils::pauseScreen();
}

std::string Authentication::loginScreen() {
    int choice;
    while(true) {
        utils::clearScreen();
        std::cout << "====================================================\n"
                  << "          EMPLOYEE PAYROLL MANAGEMENT SYSTEM\n"
                  << "                    SECURE LOGIN\n"
                  << "====================================================\n\n"
                  << "1. Login\n"
                  << "2. Continue with Google\n"
                  << "3. Forgot Password?\n"
                  << "0. Exit\n\n";
        choice = utils::getValidatedInput<int>("Enter choice: ");
        
        if (choice == 1) {
            return normalLogin();
        } else if (choice == 2) {
            return googleDemoLogin();
        } else if (choice == 3) {
            forgotPassword();
        } else if (choice == 0) {
            exit(0);
        } else {
            std::cout << "Invalid choice!\n";
            utils::pauseScreen();
        }
    }
}
