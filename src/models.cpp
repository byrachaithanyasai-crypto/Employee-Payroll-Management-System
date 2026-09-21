#include "../include/models.h"
#include <iostream>

int Employee::employeeCount = 0;

Person::Person() : age(0) {}

Person::Person(std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr)
    : fullName(name), age(a), gender(gen), phone(ph), email(em), address(addr) {}

Employee::Employee() : Person(), employeeId(0), basicSalary(0.0), status(EmploymentStatus::ACTIVE) {
    employeeCount++;
}

Employee::Employee(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
                   std::string dept, std::string desig, double salary, std::string joinDate)
    : Person(name, a, gen, ph, em, addr), employeeId(id), department(dept), designation(desig),
      basicSalary(salary), joiningDate(joinDate), status(EmploymentStatus::ACTIVE) {
    employeeCount++;
}

Employee::Employee(const Employee& other) : Person(other) {
    this->employeeId = other.employeeId;
    this->department = other.department;
    this->designation = other.designation;
    this->basicSalary = other.basicSalary;
    this->joiningDate = other.joiningDate;
    this->status = other.status;
    employeeCount++;
}

void Employee::displayDetails() const {
    std::cout << "ID: " << employeeId << " | Name: " << fullName << " | Dept: " << department 
              << " | Desig: " << designation << " | Salary: " << basicSalary << std::endl;
}

Manager::Manager(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
                 std::string dept, double salary, std::string joinDate)
    : Employee(id, name, a, gen, ph, em, addr, dept, "Manager", salary, joinDate) {}

void Manager::displayDetails() const {
    std::cout << "[Manager] ";
    Employee::displayDetails();
}

Developer::Developer(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
                 std::string dept, double salary, std::string joinDate)
    : Employee(id, name, a, gen, ph, em, addr, dept, "Developer", salary, joinDate) {}

void Developer::displayDetails() const {
    std::cout << "[Developer] ";
    Employee::displayDetails();
}

HR::HR(int id, std::string name, int a, std::string gen, std::string ph, std::string em, std::string addr,
                 std::string dept, double salary, std::string joinDate)
    : Employee(id, name, a, gen, ph, em, addr, dept, "HR", salary, joinDate) {}

void HR::displayDetails() const {
    std::cout << "[HR] ";
    Employee::displayDetails();
}

void compareSalary(const Employee& e1, const Employee& e2) {
    if (e1.basicSalary > e2.basicSalary) {
        std::cout << e1.getName() << " earns more than " << e2.getName() << std::endl;
    } else if (e1.basicSalary < e2.basicSalary) {
        std::cout << e2.getName() << " earns more than " << e1.getName() << std::endl;
    } else {
        std::cout << "Both earn the same salary." << std::endl;
    }
}
