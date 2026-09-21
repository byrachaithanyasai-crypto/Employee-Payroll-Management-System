# OOP Concept Mapping

This project explicitly demonstrates various Object-Oriented Programming (OOP) concepts in C++:

Concept                  Implementation
------------------------------------------------
Class                    `Employee`, `Person`, `PayrollManager`, `FileManager`, `AuditLogger`
Object                   Instances like `e` (Employee), `pm` (PayrollManager)
Encapsulation            Private data members in `Employee` (via protected in Person), `PayrollManager` configuration variables
Constructor              Parameterized constructor `Employee(int id, string name...)`
Destructor               Virtual destructor `virtual ~Person() = default;`
Inheritance              `Employee` inherits from `Person`. `Manager`, `Developer`, `HR` inherit from `Employee`.
Polymorphism             Virtual function `displayDetails()` implemented differently in derived classes.
Abstraction              Pure virtual function in `Person` (`virtual void displayDetails() const = 0`), making it an abstract class.
Friend Function          `friend void compareSalary(const Employee& e1, const Employee& e2)`
Operator Overloading     `bool operator==(const Employee& other) const`
Static Member            `static int employeeCount;` in `Employee`, and static methods in `FileManager`.
Exception Handling       `BaseException`, `InvalidInputException`, `AuthenticationException` used with `try-catch` blocks.
File Handling            `std::ofstream`, `std::ifstream` used in `FileManager` and `AuditLogger`.
STL                      `std::vector<Payroll>`, `std::map<int, Employee>` for dynamic collections.
Templates                Generic validation utility `template <typename T> T getValidatedInput(const std::string& prompt)` in `utils.h`.
Namespace                `namespace utils` for helper functions.
