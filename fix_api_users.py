import os

with open("src/api.cpp", "r") as f:
    api = f.read()

users_endpoints = """
    // --- USERS MANAGEMENT ---
    svr.Get("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        json arr = json::array();
        for (const auto& pair : appUsers) {
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
"""

if 'svr.Get("/api/users"' not in api:
    api = api.replace('// --- LEAVE MANAGEMENT ---', users_endpoints + '\n    // --- LEAVE MANAGEMENT ---')

with open("src/api.cpp", "w") as f:
    f.write(api)

print("Added users endpoints successfully!")
