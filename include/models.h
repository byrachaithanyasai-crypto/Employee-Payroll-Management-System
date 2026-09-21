#pragma once
#include <string>
#include <iostream>
#include <vector>

enum class EmploymentStatus { ACTIVE, INACTIVE, ON_LEAVE };

class Person {
protected:
    std::string fullName;
    int age;
    std::string gender;
    std::string phone;
    std::string email;
    std::string address;

public:
    Person();
    Person(std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr);
    virtual ~Person() = default;
    
    virtual void displayDetails() const = 0; // Pure virtual function
    
    std::string getName() const { return fullName; }
    std::string getEmail() const { return email; }
    std::string getPhone() const { return phone; }
};

class Employee : public Person {
protected:
    int employeeId;
    std::string department;
    std::string designation;
    double basicSalary;
    std::string joiningDate;
    EmploymentStatus status;
    static int employeeCount;

public:
    Employee();
    Employee(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
             std::string dept, std::string desig, double salary, std::string joinDate);
    
    // Copy constructor
    Employee(const Employee& other);
    
    virtual ~Employee() = default;

    void displayDetails() const override;
    
    int getId() const { return employeeId; }
    std::string getDepartment() const { return department; }
    std::string getDesignation() const { return designation; }
    double getBasicSalary() const { return basicSalary; }
    EmploymentStatus getStatus() const { return status; }
    
    void setStatus(EmploymentStatus s) { status = s; }
    void setBasicSalary(double salary) { basicSalary = salary; }
    
    static int getEmployeeCount() { return employeeCount; }
    
    // Operator Overloading
    bool operator==(const Employee& other) const {
        return this->employeeId == other.employeeId;
    }
    
    // Friend function
    friend void compareSalary(const Employee& e1, const Employee& e2);
};

class Manager : public Employee {
public:
    Manager(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
            std::string dept, double salary, std::string joinDate);
    void displayDetails() const override;
};

class Developer : public Employee {
public:
    Developer(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
            std::string dept, double salary, std::string joinDate);
    void displayDetails() const override;
};

class HR : public Employee {
public:
    HR(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
            std::string dept, double salary, std::string joinDate);
    void displayDetails() const override;
};

struct Attendance {
    int employeeId;
    std::string date;
    bool isPresent;
    int overtimeHours;
};

struct Payroll {
    int employeeId;
    std::string month;
    double basic;
    double hra;
    double da;
    double allowances;
    double bonus;
    double overtimePay;
    double pf;
    double tax;
    double deductions;
    double netSalary;
    bool isPaid;
};

struct User {
    std::string username;
    std::string password; // Academic demo only
    std::string role;
    std::string securityQuestion;
    std::string securityAnswer;
};
