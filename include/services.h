#pragma once
#include "models.h"
#include <map>
#include <vector>
#include <string>

class AuditLogger {
public:
    static void log(const std::string& username, const std::string& action, int empId = -1);
};

struct Settings {
    double hraPercent = 0.20;
    double daPercent = 0.10;
    double pfPercent = 0.12;
    double taxPercent = 0.05;
    double overtimeRate = 500.0;
};

class FileManager {
public:
    static void saveEmployees(const std::map<int, Employee*>& employees);
    static void loadEmployees(std::map<int, Employee*>& employees);
    static void saveAttendance(const std::vector<Attendance>& attendance);
    static void loadAttendance(std::vector<Attendance>& attendance);
    static void savePayroll(const std::vector<Payroll>& payroll);
    static void loadPayroll(std::vector<Payroll>& payroll);
    static void saveSettings(const Settings& settings);
    static void loadSettings(Settings& settings);
    static void saveUsers(const std::map<std::string, User>& users);
    static void loadUsers(std::map<std::string, User>& users);
};

class PayrollManager {
private:
    Settings settings;
public:
    PayrollManager(const Settings& s) : settings(s) {}
    Payroll calculatePayroll(const Employee& emp, const std::string& month, int otHours, double bonus, double otherDeductions);
    void generateSalarySlip(const Employee& emp, const Payroll& p);
};

class ReportManager {
public:
    static void generateEmployeeReport(const std::map<int, Employee*>& employees);
    static void generateEmployeeReport(const std::map<int, Employee*>& employees, const std::string& deptFilter);
    static void generateDepartmentReport(const std::map<int, Employee*>& employees);
    static void generateAttendanceReport(const std::vector<Attendance>& attendance);
    static void generatePayrollReport(const std::vector<Payroll>& payrolls);
};

class Authentication {
private:
    std::map<std::string, User>& users;
    
    std::string getHiddenPassword();
    void forgotPassword();
    std::string googleDemoLogin();
    std::string normalLogin();

public:
    Authentication(std::map<std::string, User>& u) : users(u) {}
    std::string loginScreen();
};
