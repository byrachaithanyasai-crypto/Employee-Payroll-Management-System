#pragma once
#include <string>
#include <exception>
#include <iostream>
#include <limits>
#include <vector>

namespace utils {
    void clearScreen();
    void pauseScreen();
    std::string getCurrentDate();
    bool isValidEmail(const std::string& email);
    bool isValidPhone(const std::string& phone);

    template <typename T>
    T getValidatedInput(const std::string& prompt) {
        T value;
        while (true) {
            std::cout << prompt;
            if (std::cin >> value) {
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                return value;
            } else {
                std::cout << "Invalid input. Please try again.\n";
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            }
        }
    }
}

class BaseException : public std::exception {
protected:
    std::string message;
public:
    BaseException(const std::string& msg) : message(msg) {}
    virtual const char* what() const noexcept override { return message.c_str(); }
};

class InvalidInputException : public BaseException {
public:
    InvalidInputException(const std::string& msg) : BaseException("Invalid Input: " + msg) {}
};

class EmployeeNotFoundException : public BaseException {
public:
    EmployeeNotFoundException(const std::string& msg) : BaseException("Employee Not Found: " + msg) {}
};

class AuthenticationException : public BaseException {
public:
    AuthenticationException(const std::string& msg) : BaseException("Authentication Error: " + msg) {}
};
