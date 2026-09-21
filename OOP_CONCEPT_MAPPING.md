# OOP Concept Mapping

This project explicitly demonstrates various Object-Oriented Programming (OOP) concepts in C++:

Concept | Class/File | Actual Implementation
--- | --- | ---
**Class** | `Employee`, `Person`, `PayrollManager`, `FileManager`, `AuditLogger` | Defined with internal logic and data members representing logical entities.
**Object** | `main.cpp` | `PayrollManager pm(appSettings);`, `Authentication auth;`, pointers in `employees` map.
**Encapsulation** | `Employee` (models.cpp) | Private/protected data members. `PayrollManager` protects configuration variables and exposes methods.
**Constructors** | `models.cpp` | `Person()`, `Employee()`, `Manager()`, `Developer()`, `HR()`.
**Parameterized constructors** | `models.cpp` | `Employee(int id, string name...)` allows setting state on creation.
**Copy constructor** | `models.cpp` | `Employee::Employee(const Employee& other)` used to safely duplicate.
**Destructor** | `models.h` / `main.cpp` | Virtual destructor `virtual ~Person() = default;` Memory cleanup on exit `delete p.second;`.
**Function overloading** | `services.cpp` | `ReportManager::generateEmployeeReport()` has two versions (one without filter, one with `deptFilter`).
**Operator overloading** | `models.h` | `bool operator==(const Employee& other) const` for comparison.
**Friend function** | `models.h` | `friend void compareSalary(const Employee& e1, const Employee& e2)`
**Static members** | `models.cpp` / `services.h` | `static int employeeCount;` in Employee, static utility methods in `FileManager`, `ReportManager`.
**Inheritance** | `models.h` | Multilevel/Hierarchical: `Employee` inherits from `Person`. `Manager`, `Developer`, `HR` inherit from `Employee`.
**Abstraction** | `models.h` | Pure virtual function `virtual void displayDetails() const = 0` in `Person`, making it an abstract class.
**Virtual functions** | `models.h` | `displayDetails` overridden in subclasses.
**Polymorphism** | `main.cpp` | Overridden `displayDetails()` is called via `Employee*` pointers in the `std::map<int, Employee*>`.
**Exception handling** | `utils.h` / `main.cpp` | Hierarchy of exceptions `BaseException`, `InvalidInputException`, `AuthenticationException`. Thrown with `throw`, caught in `try-catch` blocks.
**File handling** | `services.cpp` | `std::ofstream`, `std::ifstream` used extensively to save state as comma-separated values.
**STL vector** | `main.cpp` | `std::vector<Payroll>`, `std::vector<Attendance>`, `std::vector<LeaveRecord>`.
**STL map** | `main.cpp` | `std::map<int, Employee*>` for O(1) or O(log N) fast lookups by ID.
**STL algorithms** | `main.cpp` | `std::find_if`, `std::for_each` used for search and iteration.
**Templates** | `utils.h` | Generic function `template <typename T> T getValidatedInput(const std::string& prompt)`.
**Namespace** | `utils.h` | `namespace utils` to encapsulate helper functions.
**Scope resolution operator** | `models.cpp` | Explicitly defining functions outside class `void Employee::displayDetails()`.
