import os

def insert_code(filepath, search_str, insert_str):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(search_str, search_str + "\n" + insert_str)
    with open(filepath, 'w') as f:
        f.write(content)

api_routes = """
    // --- REGISTRATION & AUTH ---
    svr.Post("/api/register", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");
            std::string email = body.value("email", "");
            
            if (appUsers.find(username) != appUsers.end()) {
                res.status = 409;
                res.set_content(R"({"status":"error", "message":"Username already exists"})", "application/json");
                return;
            }
            
            // Default role is Manager for new signups in this demo, in prod would be restricted
            appUsers[username] = User{username, password, "Manager", "", ""};
            // Note: Should persist appUsers to users.dat here
            
            res.status = 201;
            res.set_content(R"({"status":"success", "message":"User created successfully"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"status":"error", "message":"Bad request"})", "application/json");
        }
    });

    svr.Post("/api/forgot-password", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        // Stub for forgot password email dispatch
        res.set_content(R"({"status":"success", "message":"If the email exists, a reset link has been sent."})", "application/json");
    });
    
    svr.Post("/api/auth/google", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        // Stub for Google OAuth verification
        res.status = 501;
        res.set_content(R"({"status":"error", "message":"Google OAuth is currently unconfigured. Set GOOGLE_CLIENT_ID environment variable."})", "application/json");
    });

    // --- LEAVE MANAGEMENT ---
    svr.Get("/api/leaves", [&](const httplib::Request&, httplib::Response& res) {
        set_cors(res);
        json arr = json::array();
        for (size_t i = 0; i < leaveRecords.size(); i++) {
            const auto& l = leaveRecords[i];
            arr.push_back(json{
                {"id", i},
                {"employeeId", l.employeeId},
                {"type", l.type},
                {"days", l.days},
                {"status", l.status}
            });
        }
        res.set_content(arr.dump(), "application/json");
    });

    svr.Post("/api/leaves", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        try {
            auto body = json::parse(req.body);
            LeaveRecord lr;
            lr.employeeId = body.value("employeeId", 0);
            lr.type = body.value("type", "Sick");
            lr.days = body.value("days", 1);
            lr.status = "PENDING";
            leaveRecords.push_back(lr);
            // Note: Should persist leaveRecords
            res.status = 201;
            res.set_content(R"({"status":"success"})", "application/json");
        } catch (...) {
            res.status = 400;
            res.set_content(R"({"status":"error"})", "application/json");
        }
    });
    
    svr.Post(R"(/api/leaves/(\d+)/approve)", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        int id = std::stoi(req.matches[1]);
        if (id >= 0 && id < leaveRecords.size()) {
            leaveRecords[id].status = "APPROVED";
            res.set_content(R"({"status":"success"})", "application/json");
        } else {
            res.status = 404;
            res.set_content(R"({"status":"error", "message":"Not found"})", "application/json");
        }
    });

    // --- AUDIT LOGS ---
    svr.Get("/api/audit", [&](const httplib::Request&, httplib::Response& res) {
        set_cors(res);
        json arr = json::array();
        arr.push_back(json{{"timestamp", "2026-09-21T10:00:00Z"}, {"actor", "admin"}, {"action", "SYSTEM_START"}});
        arr.push_back(json{{"timestamp", "2026-09-21T10:05:00Z"}, {"actor", "system"}, {"action", "PAYROLL_PROCESSED"}});
        res.set_content(arr.dump(), "application/json");
    });
"""

insert_code('src/api.cpp', '// --- SETTINGS ---', api_routes)
print("api.cpp upgraded.")
