import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Split-Screen Login Redesign
write_file("frontend/src/pages/Login.jsx", """
import React, { useState } from 'react';
import axios from 'axios';
import { Lock, User, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const res = await axios.post('http://localhost:8080/api/login', { username, password });
      if (res.data.status === 'success') onLogin(res.data);
    } catch (err) { setError(err.response?.data?.message || 'Connection to API failed.'); }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Branding Side */}
      <div className="hidden lg:flex w-1/2 bg-slate-900 flex-col justify-center items-center p-12 text-center relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-blue-600"></div>
        <div className="z-10 text-white space-y-6 max-w-lg">
          <h1 className="text-6xl font-bold tracking-wider text-blue-500">EPMS</h1>
          <h2 className="text-3xl font-semibold">Employee Payroll Management System</h2>
          <p className="text-slate-400 text-lg leading-relaxed">
            The complete professional solution for payroll processing, employee management, and human resources administration.
          </p>
        </div>
        <div className="absolute bottom-0 opacity-10 pointer-events-none">
          <svg width="600" height="600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
        </div>
      </div>

      {/* Right Login Side */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-gray-50 p-8">
        <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl">
          <div className="lg:hidden text-center mb-8">
            <h1 className="text-4xl font-bold text-blue-600 tracking-wider mb-2">EPMS</h1>
            <p className="text-slate-600">Employee Payroll Management System</p>
          </div>
          
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Sign In</h2>
          
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 flex items-center text-red-700">
              <AlertCircle size={20} className="mr-2" /><span className="text-sm font-medium">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <div className="relative">
                <User size={18} className="absolute left-3 top-3.5 text-gray-400" />
                <input type="text" required className="pl-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={username} onChange={e => setUsername(e.target.value)} />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <Lock size={18} className="absolute left-3 top-3.5 text-gray-400" />
                <input type={showPassword ? "text" : "password"} required className="pl-10 pr-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600 outline-none" value={password} onChange={e => setPassword(e.target.value)} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600">
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              <div className="text-right mt-2">
                <a href="#" className="text-sm font-medium text-blue-600 hover:underline">Forgot Password?</a>
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-all disabled:opacity-70 flex justify-center">
              {loading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : 'Sign In'}
            </button>
            
            <button type="button" className="w-full bg-white border border-gray-300 text-gray-700 font-semibold py-3 rounded-lg hover:bg-gray-50 transition-all flex items-center justify-center space-x-2">
              <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
              <span>Sign in with Google</span>
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-gray-500">
            Don't have an account? <Link to="/register" className="text-blue-600 font-semibold hover:underline">Create Account</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
""")

# 2. Users Management Component
write_file("frontend/src/pages/Users.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, UserPlus, Shield } from 'lucide-react';

export default function Users() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    axios.get('http://localhost:8080/api/users').then(res => setUsers(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border">
        <div>
          <h2 className="text-xl font-bold text-slate-800">User Accounts</h2>
          <p className="text-sm text-gray-500">Manage system access and roles</p>
        </div>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2"><UserPlus size={18}/><span>Add User</span></button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b">
            <tr>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Username</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Role</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-center">Security</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {users.map((u, i) => (
              <tr key={i}>
                <td className="px-6 py-4 font-bold">{u.username}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${u.role==='Admin'?'bg-red-100 text-red-800':u.role==='HR'?'bg-purple-100 text-purple-800':'bg-blue-100 text-blue-800'}`}>
                    {u.role}
                  </span>
                </td>
                <td className="px-6 py-4 text-center">
                  <button className="text-slate-400 hover:text-blue-600"><Shield size={18}/></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
""")

# 3. Settings Component
write_file("frontend/src/pages/Settings.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Save } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({ hraPercent: 0, daPercent: 0, pfPercent: 0, taxPercent: 0, overtimeRate: 0 });

  useEffect(() => {
    axios.get('http://localhost:8080/api/settings').then(res => setSettings(res.data)).catch(console.error);
  }, []);

  return (
    <div className="max-w-2xl bg-white rounded-xl shadow-sm border p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-6">Payroll Configuration</h2>
      <form className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">HRA Percentage (%)</label>
            <input type="number" className="w-full border rounded-lg p-2" value={settings.hraPercent} onChange={e => setSettings({...settings, hraPercent: parseFloat(e.target.value)})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">DA Percentage (%)</label>
            <input type="number" className="w-full border rounded-lg p-2" value={settings.daPercent} onChange={e => setSettings({...settings, daPercent: parseFloat(e.target.value)})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">PF Percentage (%)</label>
            <input type="number" className="w-full border rounded-lg p-2" value={settings.pfPercent} onChange={e => setSettings({...settings, pfPercent: parseFloat(e.target.value)})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Tax Percentage (%)</label>
            <input type="number" className="w-full border rounded-lg p-2" value={settings.taxPercent} onChange={e => setSettings({...settings, taxPercent: parseFloat(e.target.value)})} />
          </div>
        </div>
        <button type="button" className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center space-x-2 mt-4 hover:bg-blue-700">
          <Save size={18}/><span>Save Settings</span>
        </button>
      </form>
    </div>
  );
}
""")

# 4. Audit Log Component
write_file("frontend/src/pages/AuditLog.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity } from 'lucide-react';

export default function AuditLog() {
  const [logs, setLogs] = useState([]);
  
  useEffect(() => {
    axios.get('http://localhost:8080/api/audit').then(res => setLogs(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border">
        <h2 className="text-xl font-bold text-slate-800 flex items-center"><Activity className="mr-2" size={20}/> System Audit Logs</h2>
      </div>
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b">
            <tr>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Timestamp (UTC)</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Actor</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Action Event</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {logs.map((l, i) => (
              <tr key={i} className="hover:bg-slate-50">
                <td className="px-6 py-4 text-sm text-gray-500">{l.timestamp}</td>
                <td className="px-6 py-4 text-sm font-semibold">{l.actor}</td>
                <td className="px-6 py-4 text-sm"><span className="px-2 py-1 bg-gray-100 rounded text-xs font-mono">{l.action}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
""")

# Update Layout and App to include these routes
with open("frontend/src/layouts/Layout.jsx", "r") as f:
    layout = f.read()
layout = layout.replace("import { Calendar } from 'lucide-react';", "import { Calendar, Users as UsersIcon, Settings as SettingsIcon, Activity } from 'lucide-react';")
layout = layout.replace("{ name: 'Leaves', path: '/leaves', icon: Calendar },", """{ name: 'Leaves', path: '/leaves', icon: Calendar },
    { name: 'Users', path: '/users', icon: UsersIcon },
    { name: 'Settings', path: '/settings', icon: SettingsIcon },
    { name: 'Audit Logs', path: '/audit', icon: Activity },""")
write_file("frontend/src/layouts/Layout.jsx", layout)

with open("frontend/src/App.jsx", "r") as f:
    app = f.read()
app = app.replace("import Leaves from './pages/Leaves';", """import Leaves from './pages/Leaves';
import Users from './pages/Users';
import Settings from './pages/Settings';
import AuditLog from './pages/AuditLog';""")
app = app.replace("<Route path=\"/leaves\" element={<Leaves />} />", """<Route path="/leaves" element={<Leaves />} />
            <Route path="/users" element={<Users />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/audit" element={<AuditLog />} />""")
write_file("frontend/src/App.jsx", app)

print("Ultimate React components generated!")
