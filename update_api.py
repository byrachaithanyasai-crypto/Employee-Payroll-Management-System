import re
import os

with open("src/api.cpp", "r") as f:
    api = f.read()

# 1. Update GET /api/users to hide admin
hide_admin_get = """
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
"""

# We replace the entire GET block
api = re.sub(r'svr\.Get\("/api/users",.*?\);', hide_admin_get.strip(), api, flags=re.DOTALL)

# 2. Add DELETE /api/users/:username logic
delete_logic = """
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

if 'svr.Delete(R"(/api/users/' not in api:
    # Insert right after POST /api/users
    match = re.search(r'svr\.Post\("/api/users",.*?\);', api, flags=re.DOTALL)
    if match:
        end_idx = match.end()
        api = api[:end_idx] + "\n\n" + delete_logic + api[end_idx:]
    else:
        print("COULD NOT FIND POST /api/users")
        exit(1)

with open("src/api.cpp", "w") as f:
    f.write(api)

print("Backend API updated successfully!")
