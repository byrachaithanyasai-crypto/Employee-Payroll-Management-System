import os
import re

# 1. Update Layout.jsx to remove Audit Logs
layout_path = "frontend/src/layouts/Layout.jsx"
with open(layout_path, "r") as f:
    layout = f.read()
layout = layout.replace(", Activity", "")
layout = re.sub(r"\{\s*name:\s*'Audit Logs',\s*path:\s*'/audit',\s*icon:\s*Activity\s*\},?", "", layout)
with open(layout_path, "w") as f:
    f.write(layout)

# 2. Update App.jsx to remove Audit Logs
app_path = "frontend/src/App.jsx"
with open(app_path, "r") as f:
    app = f.read()
app = app.replace("import AuditLog from './pages/AuditLog';\n", "")
app = re.sub(r"<Route\s+path=\"/audit\"\s+element=\{<AuditLog\s*/>\}\s*/>", "", app)
with open(app_path, "w") as f:
    f.write(app)

# 3. Delete AuditLog.jsx
audit_path = "frontend/src/pages/AuditLog.jsx"
if os.path.exists(audit_path):
    os.remove(audit_path)

# 4. Overhaul Employees.jsx to have a working Add Employee modal
employees_code = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, UserPlus, MoreVertical, X, CheckCircle, AlertCircle } from 'lucide-react';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });
  const [formData, setFormData] = useState({ id: '', name: '', department: 'IT', designation: 'Developer', salary: '' });

  const fetchEmployees = () => {
    axios.get('http://localhost:8080/api/employees').then(res => setEmployees(res.data)).catch(console.error);
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...formData, id: parseInt(formData.id), salary: parseFloat(formData.salary) };
      await axios.post('http://localhost:8080/api/employees', payload);
      setShowModal(false);
      setFormData({ id: '', name: '', department: 'IT', designation: 'Developer', salary: '' });
      fetchEmployees();
      showToast('success', 'Employee created successfully.');
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to create employee.');
    }
    setLoading(false);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this employee?")) {
      try {
        await axios.delete(`http://localhost:8080/api/employees/${id}`);
        fetchEmployees();
        showToast('success', 'Employee deleted successfully.');
      } catch (err) {
        showToast('error', 'Failed to delete employee.');
      }
    }
  };

  return (
    <div className="space-y-6">
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center space-x-2 text-white ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-medium">{notification.msg}</span>
        </div>
      )}

      <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Employees</h2>
          <p className="text-slate-500 mt-1 text-sm">Manage company personnel records</p>
        </div>
        <button onClick={() => setShowModal(true)} className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm flex items-center space-x-2">
          <UserPlus size={18}/>
          <span>Add Employee</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-4 border-b flex items-center justify-between bg-slate-50">
          <div className="relative w-64">
            <Search className="absolute left-3 top-2.5 text-slate-400" size={18}/>
            <input type="text" placeholder="Search employees..." className="pl-10 pr-4 py-2 w-full border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-600 bg-white" />
          </div>
        </div>
        
        {employees.length === 0 ? (
          <div className="p-12 text-center text-slate-500">
            <p className="text-lg font-medium mb-2">No employees found</p>
            <p className="text-sm">Click "Add Employee" to create a new personnel record.</p>
          </div>
        ) : (
          <table className="w-full text-left">
            <thead className="bg-slate-100 border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">ID</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Name</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Department</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Designation</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Base Salary</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {employees.map(e => (
                <tr key={e.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 font-semibold text-slate-700">#{e.id}</td>
                  <td className="px-6 py-4 font-medium text-slate-900">{e.name}</td>
                  <td className="px-6 py-4 text-slate-600">{e.department}</td>
                  <td className="px-6 py-4 text-slate-600">{e.designation}</td>
                  <td className="px-6 py-4 font-mono text-slate-700">₹{e.salary.toLocaleString('en-IN')}</td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => handleDelete(e.id)} className="text-red-500 hover:text-red-700 text-sm font-medium transition-colors">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-40 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50">
              <h3 className="text-xl font-bold text-slate-800">Add New Employee</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 transition-colors"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Employee ID</label>
                <input type="number" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.id} onChange={e => setFormData({...formData, id: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Full Name</label>
                <input type="text" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Department</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none bg-white" value={formData.department} onChange={e => setFormData({...formData, department: e.target.value})}>
                    <option>IT</option>
                    <option>HR</option>
                    <option>Finance</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Designation</label>
                  <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none bg-white" value={formData.designation} onChange={e => setFormData({...formData, designation: e.target.value})}>
                    <option>Developer</option>
                    <option>Manager</option>
                    <option>HR</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Base Salary (₹)</label>
                <input type="number" step="0.01" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.salary} onChange={e => setFormData({...formData, salary: e.target.value})} />
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 border rounded-lg font-medium text-slate-600 hover:bg-slate-50 transition-colors">Cancel</button>
                <button type="submit" disabled={loading} className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center justify-center min-w-[120px]">
                  {loading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : 'Save Employee'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
"""
with open("frontend/src/pages/Employees.jsx", "w", encoding="utf-8") as f:
    f.write(employees_code)


# 5. Overhaul Users.jsx to have a working Add User modal
users_code = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, UserPlus, X, CheckCircle, AlertCircle } from 'lucide-react';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });
  const [formData, setFormData] = useState({ username: '', password: '', confirm: '', role: 'Manager' });

  const fetchUsers = () => {
    axios.get('http://localhost:8080/api/users').then(res => setUsers(res.data)).catch(console.error);
  };

  useEffect(() => { fetchUsers(); }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(formData.password !== formData.confirm) return showToast('error', 'Passwords do not match');
    setLoading(true);
    try {
      await axios.post('http://localhost:8080/api/users', { username: formData.username, password: formData.password, role: formData.role });
      setShowModal(false);
      setFormData({ username: '', password: '', confirm: '', role: 'Manager' });
      fetchUsers();
      showToast('success', 'System user created successfully.');
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to create user.');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center space-x-2 text-white ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-medium">{notification.msg}</span>
        </div>
      )}

      <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">System Users</h2>
          <p className="text-slate-500 mt-1 text-sm">Manage system access and authentication roles</p>
        </div>
        <button onClick={() => setShowModal(true)} className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm flex items-center space-x-2">
          <UserPlus size={18}/>
          <span>Add User</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-100 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Username</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider">Role</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">Security Level</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {users.map((u, i) => (
              <tr key={i} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 font-bold text-slate-800">{u.username}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    u.role.toUpperCase() === 'ADMIN' ? 'bg-red-100 text-red-800' : 
                    u.role.toUpperCase() === 'HR' ? 'bg-purple-100 text-purple-800' : 
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {u.role.toUpperCase()}
                  </span>
                </td>
                <td className="px-6 py-4 text-center">
                  <Shield size={18} className="mx-auto text-slate-400"/>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-40 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50">
              <h3 className="text-xl font-bold text-slate-800">Create System User</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 transition-colors"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Username</label>
                <input type="text" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Role</label>
                <select className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none bg-white" value={formData.role} onChange={e => setFormData({...formData, role: e.target.value})}>
                  <option value="Manager">Manager</option>
                  <option value="HR">HR</option>
                  <option value="Admin">Admin</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Password</label>
                <input type="password" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Confirm Password</label>
                <input type="password" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={formData.confirm} onChange={e => setFormData({...formData, confirm: e.target.value})} />
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 border rounded-lg font-medium text-slate-600 hover:bg-slate-50 transition-colors">Cancel</button>
                <button type="submit" disabled={loading} className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center justify-center min-w-[120px]">
                  {loading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : 'Create User'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
"""
with open("frontend/src/pages/Users.jsx", "w", encoding="utf-8") as f:
    f.write(users_code)

# 6. Update api.cpp to actually save appUsers when /api/register or /api/users is called
api_path = "src/api.cpp"
with open(api_path, "r") as f:
    api = f.read()

# Replace the stub persistence comment with actual persistence call in /api/register
api = api.replace("// Note: Should persist appUsers to users.dat here", "FileManager::saveUsers(appUsers);")

# Add POST /api/users
api_users_post = """
    svr.Post("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        set_cors(res);
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");
            std::string role = body.value("role", "Manager");
            
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

if 'svr.Post("/api/users"' not in api:
    # Insert it right before GET /api/users
    api = api.replace('svr.Get("/api/users"', api_users_post + '\n    svr.Get("/api/users"')

with open(api_path, "w") as f:
    f.write(api)

print("Upgrade finished.")
