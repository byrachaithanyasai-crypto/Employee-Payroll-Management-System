#include "../include/api.h"
#include "../include/httplib.h"
#include "../include/json.hpp"
#include "../include/services.h"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <random>
#include <unordered_map>

using json = nlohmann::json;

extern std::map<int, Employee*> employees;
extern std::vector<Attendance> attendanceRecords;
extern std::vector<Payroll> payrollRecords;
extern Settings appSettings;



std::unordered_map<std::string, std::string> activeSessions;

std::string generateSessionToken() {
    const char alphanum[] =
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    std::string token(32, '0');

    std::random_device rd;

    for (int i = 0; i < 32; ++i) {
        token[i] = alphanum[rd() % 62];
    }

    return token;
}

void set_cors(httplib::Response& res) {
    res.set_header("Access-Control-Allow-Origin", "*");
    res.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
    res.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization");
}

std::string get_role(const httplib::Request& req, const std::map<std::string, User>& appUsers, std::string* outUsername = nullptr) {
    std::string authHeader = req.has_header("Authorization") ? req.get_header_value("Authorization") : "";
    std::string currentUser = "";
    std::string currentRole = "";
    
    if (authHeader.find("Bearer ") == 0) {
        std::string token = authHeader.substr(7);
        if (activeSessions.find(token) != activeSessions.end()) {
            currentUser = activeSessions[token];
            if (appUsers.find(currentUser) != appUsers.end()) {
                currentRole = appUsers.at(currentUser).role;
                if (outUsername) *outUsername = currentUser;
            }
        }
    }
    std::transform(currentRole.begin(), currentRole.end(), currentRole.begin(), ::toupper);
    return currentRole;
}

void startApiServer(int port, std::map<std::string, User>& appUsers) {
    httplib::Server svr;

    svr.Options(R"(.*)", [](const httplib::Request&, httplib::Response& res) {
        set_cors(res);
    });

    // --- AUTHENTICATION ---
    svr.Post("/api/login", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");

            auto it = appUsers.find(username);
            if (it != appUsers.end() && it->second.password == password) {
                std::string token = generateSessionToken();
                activeSessions[token] = username;
                
                json response = {
                    {"status", "success"},
                    {"role", it->second.role},
                    {"username", username},
                    {"token", token} 
                };
                res.set_content(response.dump(), "application/json");
            } else {
                res.status = 401;
                res.set_content(R"({"status":"error", "message":"Invalid credentials"})", "application/json");
            }
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"status":"error", "message":"Bad request"})", "application/json");
        }
    });

    // --- DASHBOARD STATS ---
    svr.Get("/api/stats", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role.empty()) {
            res.status = 401;
            res.set_content(R"({"message":"Unauthorized"})", "application/json");
            return;
        }

        double totalPayroll = 0;
        double avgSalary = 0;
        for (const auto& p : employees) {
            totalPayroll += p.second->getBasicSalary();
        }
        if (!employees.empty()) avgSalary = totalPayroll / employees.size();

        json stats = {
            {"totalEmployees", employees.size()},
            {"activeEmployees", employees.size()},
            {"totalPayroll", totalPayroll},
            {"avgSalary", avgSalary}
        };
        res.set_content(stats.dump(), "application/json");
    });

    // --- EMPLOYEES ---
    svr.Get("/api/employees", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR" && role != "MANAGER") {
            res.status = 403;
            res.set_content(R"({"message":"Administrator privileges required"})", "application/json");
            return;
        }

        json arr = json::array();
        for (const auto& pair : employees) {
            Employee* e = pair.second;
            arr.push_back(json{
                {"id", e->getId()},
                {"name", e->getName()},
                {"department", e->getDepartment()},
                {"designation", e->getDesignation()},
                {"basicSalary", e->getBasicSalary()}
            });
        }
        res.set_content(arr.dump(), "application/json");
    });

    svr.Post("/api/employees", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        try {
            auto body = json::parse(req.body);
            int id = body.value("id", 0);
            std::string name = body.value("name", "");
            std::string dept = body.value("department", "");
            std::string desig = body.value("designation", "");
            double salary = body.value("basicSalary", 0.0);

            if (employees.find(id) != employees.end()) {
                res.status = 409;
                res.set_content(R"({"message":"Employee ID already exists"})", "application/json");
                return;
            }
            
            Employee* newE = nullptr;
            if (desig == "Manager" || desig == "MANAGER") {
                newE = new Manager(id, name, 30, "Unknown", "N/A", "N/A", "N/A", dept, salary, "2026-01-01");
            } else if (desig == "HR") {
                newE = new HR(id, name, 30, "Unknown", "N/A", "N/A", "N/A", dept, salary, "2026-01-01");
            } else {
                newE = new Developer(id, name, 30, "Unknown", "N/A", "N/A", "N/A", dept, salary, "2026-01-01");
            }
            employees[id] = newE;
            FileManager::saveEmployees(employees);
            
            res.status = 201;
            res.set_content(R"({"status":"success"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"message":"Invalid payload"})", "application/json");
        }
    });

    svr.Put(R"(/api/employees/(\d+))", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        try {
            int id = std::stoi(req.matches[1]);
            auto body = json::parse(req.body);
            if (employees.find(id) == employees.end()) {
                res.status = 404;
                res.set_content(R"({"message":"Employee not found"})", "application/json");
                return;
            }
            
            Employee* oldE = employees[id];
            std::string newName = body.value("name", oldE->getName());
            std::string newDept = body.value("department", oldE->getDepartment());
            std::string newDesig = body.value("designation", oldE->getDesignation());
            double newSal = body.value("basicSalary", oldE->getBasicSalary());
            
            Employee* newE = nullptr;
            if (newDesig == "Manager" || newDesig == "MANAGER") {
                newE = new Manager(id, newName, 30, "Unknown", "N/A", "N/A", "N/A", newDept, newSal, "2026-01-01");
            } else if (newDesig == "HR") {
                newE = new HR(id, newName, 30, "Unknown", "N/A", "N/A", "N/A", newDept, newSal, "2026-01-01");
            } else {
                newE = new Developer(id, newName, 30, "Unknown", "N/A", "N/A", "N/A", newDept, newSal, "2026-01-01");
            }
            
            delete employees[id];
            employees[id] = newE;
            
            FileManager::saveEmployees(employees);
            res.set_content(R"({"status":"success"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"message":"Invalid payload"})", "application/json");
        }
    });

    svr.Delete(R"(/api/employees/(\d+))", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        int id = std::stoi(req.matches[1]);
        if (employees.find(id) != employees.end()) {
            delete employees[id];
            employees.erase(id);
            FileManager::saveEmployees(employees);
            res.set_content(R"({"status":"success"})", "application/json");
        } else {
            res.status = 404;
            res.set_content(R"({"message":"Employee not found"})", "application/json");
        }
    });

    // --- PAYROLL ---
    svr.Get("/api/payroll", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR" && role != "MANAGER") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        json arr = json::array();
        for (const auto& p : payrollRecords) {
            arr.push_back(json{
                {"employeeId", p.employeeId},
                {"month", p.month},
                {"year", "2026"},
                {"basicSalary", p.basic},
                {"hra", p.hra},
                {"da", p.da},
                {"pf", p.pf},
                {"tax", p.tax},
                {"netSalary", p.netSalary},
                {"status", p.isPaid ? "Paid" : "Pending"}
            });
        }
        res.set_content(arr.dump(), "application/json");
    });

    svr.Post("/api/payroll/process", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        try {
            std::string month = "Current Month"; // Default
            
            payrollRecords.clear(); // Recompute for simplicity in demo
            for (const auto& pair : employees) {
                Employee* e = pair.second;
                Payroll p;
                p.employeeId = e->getId();
                p.month = month;
                p.basic = e->getBasicSalary();
                p.hra = p.basic * (appSettings.hraPercent / 100.0);
                p.da = p.basic * (appSettings.daPercent / 100.0);
                p.pf = p.basic * (appSettings.pfPercent / 100.0);
                
                double gross = p.basic + p.hra + p.da;
                p.tax = gross * (appSettings.taxPercent / 100.0);
                p.netSalary = gross - (p.pf + p.tax);
                p.isPaid = true;
                
                payrollRecords.push_back(p);
            }
            FileManager::savePayroll(payrollRecords);
            res.set_content(R"({"status":"success"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"message":"Failed to process payroll"})", "application/json");
        }
    });

    // --- USERS MANAGEMENT ---
    svr.Get("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN" && role != "HR" && role != "MANAGER") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        json arr = json::array();
        for (const auto& pair : appUsers) {
            if (pair.first == "admin") continue; // HIDE ADMIN
            arr.push_back(json{
                {"username", pair.second.username},
                {"role", pair.second.role}
            });
        }
        res.set_content(arr.dump(), "application/json");
    });

    svr.Post("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN") {
            res.status = 403;
            res.set_content(R"({"message":"You do not have permission to perform this action."})", "application/json");
            return;
        }

        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");
            std::string newRole = body.value("role", "Manager");
            
            if (username.empty() || password.empty()) {
                res.status = 400;
                res.set_content(R"({"status":"error", "message":"Username and password are required"})", "application/json");
                return;
            }
            
            if (appUsers.find(username) != appUsers.end()) {
                res.status = 409;
                res.set_content(R"({"status":"error", "message":"Username already exists"})", "application/json");
                return;
            }
            
            appUsers[username] = User{username, password, newRole, "", ""};
            FileManager::saveUsers(appUsers);
            
            res.status = 201;
            res.set_content(R"({"status":"success", "message":"User created successfully"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"status":"error", "message":"Bad request"})", "application/json");
        }
    });

    svr.Delete(R"(/api/users/([^/]+))", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string targetUsername = req.matches[1];
        
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN") {
            res.status = 403;
            res.set_content(R"({"success":false, "message":"Administrator privileges required"})", "application/json");
            return;
        }
        
        if (targetUsername == "admin") {
            res.status = 403;
            res.set_content(R"({"success":false, "message":"The built-in administrator account cannot be deleted"})", "application/json");
            return;
        }
        
        auto it = appUsers.find(targetUsername);
        if (it != appUsers.end()) {
            appUsers.erase(it);
            FileManager::saveUsers(appUsers);
            res.set_content(R"({"success":true, "message":"User deleted successfully"})", "application/json");
        } else {
            res.status = 404;
            res.set_content(R"({"success":false, "message":"User not found"})", "application/json");
        }
    });

    // --- SETTINGS ---
    svr.Get("/api/settings", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        json s = {
            {"hraPercent", appSettings.hraPercent * 100.0},
            {"daPercent", appSettings.daPercent * 100.0},
            {"pfPercent", appSettings.pfPercent * 100.0},
            {"taxPercent", appSettings.taxPercent * 100.0}
        };
        res.set_content(s.dump(), "application/json");
    });
    
    svr.Post("/api/settings", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        std::string role = get_role(req, appUsers);
        if (role != "ADMIN") {
            res.status = 403;
            res.set_content(R"({"success":false, "message":"Administrator privileges required"})", "application/json");
            return;
        }
        
        try {
            auto body = json::parse(req.body);
            appSettings.hraPercent = body.value("hraPercent", appSettings.hraPercent * 100.0) / 100.0;
            appSettings.daPercent = body.value("daPercent", appSettings.daPercent * 100.0) / 100.0;
            appSettings.pfPercent = body.value("pfPercent", appSettings.pfPercent * 100.0) / 100.0;
            appSettings.taxPercent = body.value("taxPercent", appSettings.taxPercent * 100.0) / 100.0;
            FileManager::saveSettings(appSettings);
            res.set_content(R"({"status":"success"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"message":"Invalid payload"})", "application/json");
        }
    });

    std::cout << "Starting Professional C++ API Server on http://localhost:" << port << "..." << std::endl;
    std::cout << "Press Ctrl+C to stop." << std::endl;
    svr.listen("0.0.0.0", port);
}
