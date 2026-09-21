#include "../include/utils.h"
#include <ctime>
#include <cstdlib>
#include <regex>

namespace utils {
    void clearScreen() {
#ifdef _WIN32
        std::system("cls");
#else
        std::system("clear");
#endif
    }

    void pauseScreen() {
        std::cout << "\nPress Enter to continue...";
        std::string dummy;
        std::getline(std::cin, dummy);
    }

    std::string getCurrentDate() {
        time_t now = time(0);
        tm* ltm = localtime(&now);
        char buffer[80];
        strftime(buffer, sizeof(buffer), "%Y-%m-%d", ltm);
        return std::string(buffer);
    }

    bool isValidEmail(const std::string& email) {
        const std::regex pattern("(\\w+)(\\.|_)?(\\w*)@(\\w+)(\\.(\\w+))+");
        return std::regex_match(email, pattern);
    }

    bool isValidPhone(const std::string& phone) {
        return phone.length() >= 10;
    }
}
