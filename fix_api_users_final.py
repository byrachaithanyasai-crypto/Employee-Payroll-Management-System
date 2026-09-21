import re

with open("src/api.cpp", "r") as f:
    api = f.read()

# We need to completely rewrite the users section.
# First, let's remove everything from `// --- USERS MANAGEMENT ---` down to `// --- LEAVE MANAGEMENT ---`
start_idx = api.find('// --- USERS MANAGEMENT ---')
end_idx = api.find('// --- LEAVE MANAGEMENT ---')

if start_idx != -1 and end_idx != -1:
    clean_api = api[:start_idx] + "\n" + api[end_idx:]
else:
    print("Could not find blocks")
    exit(1)

users_management_code = """    // --- USERS MANAGEMENT ---
    svr.Get("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
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
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");
            std::string role = body.value("role", "Manager");
            
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
            
            appUsers[username] = User{username, password, role, "", ""};
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
        
        // --- AUTHORIZATION CHECK ---
        std::string authHeader = req.has_header("Authorization") ? req.get_header_value("Authorization") : "";
        std::string currentUser = "";
        std::string currentRole = "";
        
        // Parse "Bearer username_secure_token_abc123"
        if (authHeader.find("Bearer ") == 0) {
            std::string token = authHeader.substr(7);
            size_t pos = token.find("_secure_token_abc123");
            if (pos != std::string::npos) {
                currentUser = token.substr(0, pos);
                if (appUsers.find(currentUser) != appUsers.end()) {
                    currentRole = appUsers[currentUser].role;
                }
            }
        }
        
        // Only Admin can delete
        if (currentRole != "Admin" && currentRole != "ADMIN") {
            res.status = 403;
            res.set_content(R"({"success":false, "message":"Administrator privileges required"})", "application/json");
            return;
        }
        
        // Protect built-in admin account
        if (targetUsername == "admin") {
            res.status = 403;
            res.set_content(R"({"success":false, "message":"The built-in administrator account cannot be deleted"})", "application/json");
            return;
        }
        
        // Perform deletion
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

"""

# Insert it back
clean_api = clean_api.replace('// --- LEAVE MANAGEMENT ---', users_management_code + '\n    // --- LEAVE MANAGEMENT ---')

with open("src/api.cpp", "w") as f:
    f.write(clean_api)

print("Fixed API successfully")
