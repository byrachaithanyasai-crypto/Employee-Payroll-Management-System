import os

def insert_code(filepath, search_str, insert_str):
    with open(filepath, 'r') as f:
        content = f.read()
    if insert_str not in content:
        content = content.replace(search_str, search_str + "\n" + insert_str)
        with open(filepath, 'w') as f:
            f.write(content)

backend_users = """
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
"""

insert_code('src/api.cpp', '// --- SETTINGS ---', backend_users)
print("api.cpp updated with /api/users endpoint.")
