import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Wrote {path}")

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {path}")

# =======================
# UTILS
# =======================
auth_js = """
// RBAC Utilities
export const ROLES = {
  ADMIN: 'ADMIN',
  HR: 'HR',
  MANAGER: 'MANAGER'
};

export const PERMISSIONS = {
  DASHBOARD_FULL: 'DASHBOARD_FULL',
  EMPLOYEES_CREATE: 'EMPLOYEES_CREATE',
  EMPLOYEES_EDIT: 'EMPLOYEES_EDIT',
  EMPLOYEES_DELETE: 'EMPLOYEES_DELETE',
  PAYROLL_PROCESS: 'PAYROLL_PROCESS',
  PAYROLL_EDIT: 'PAYROLL_EDIT',
  USERS_VIEW: 'USERS_VIEW',
  USERS_CREATE: 'USERS_CREATE',
  USERS_DELETE: 'USERS_DELETE',
  SETTINGS_ADMIN: 'SETTINGS_ADMIN'
};

const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: Object.values(PERMISSIONS),
  [ROLES.HR]: [
    PERMISSIONS.EMPLOYEES_CREATE,
    PERMISSIONS.EMPLOYEES_EDIT,
    PERMISSIONS.PAYROLL_PROCESS,
    PERMISSIONS.PAYROLL_EDIT,
    PERMISSIONS.USERS_VIEW
  ],
  [ROLES.MANAGER]: [
    PERMISSIONS.USERS_VIEW // Very restricted
  ]
};

export const hasPermission = (role, permission) => {
  const normalizedRole = String(role).toUpperCase();
  const permissions = ROLE_PERMISSIONS[normalizedRole] || [];
  return permissions.includes(permission);
};
"""

# =======================
# APP
# =======================
app_jsx = """
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layouts/Layout';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Payroll from './pages/Payroll';
import Users from './pages/Users';
import Settings from './pages/Settings';
import Login from './pages/Login';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="employees" element={<Employees />} />
          <Route path="payroll" element={<Payroll />} />
          <Route path="users" element={<Users />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
"""

# =======================
# LAYOUT
# =======================
layout_jsx = """
import React from 'react';
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users as UsersIcon, 
  CreditCard, 
  Settings as SettingsIcon, 
  LogOut,
  ShieldAlert
} from 'lucide-react';
import { hasPermission, PERMISSIONS } from '../utils/auth';

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = localStorage.getItem('role') || 'Unknown';
  const username = localStorage.getItem('username') || 'User';

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Employees', path: '/employees', icon: UsersIcon },
    { name: 'Payroll', path: '/payroll', icon: CreditCard },
  ];

  // Users page is visible to all basic roles but functionality inside is restricted
  if (hasPermission(role, PERMISSIONS.USERS_VIEW)) {
    navItems.push({ name: 'User Management', path: '/users', icon: ShieldAlert });
  }
  
  navItems.push({ name: 'Settings', path: '/settings', icon: SettingsIcon });

  const currentPathName = navItems.find(i => i.path === location.pathname)?.name || 'EPMS';

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col transition-all duration-300 hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl leading-none">E</span>
            </div>
            <span className="text-white font-bold text-lg tracking-wide">EPMS</span>
          </div>
        </div>
        
        <nav className="flex-1 py-6 px-4 flex flex-col gap-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                    isActive 
                      ? 'bg-blue-600 text-white font-medium shadow-md shadow-blue-900/20' 
                      : 'hover:bg-slate-800 hover:text-white'
                  }`
                }
              >
                <Icon size={20} className="shrink-0" />
                <span className="truncate">{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-slate-800">
          <button 
            onClick={handleLogout}
            className="flex items-center space-x-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:bg-slate-800 hover:text-white transition-all duration-200"
          >
            <LogOut size={20} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0 z-10">
          <h1 className="text-xl font-bold text-slate-800 hidden sm:block">{currentPathName}</h1>
          
          <div className="flex items-center space-x-4 ml-auto">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-bold text-slate-800 leading-tight">{username}</p>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{role}</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold border border-blue-200 shrink-0">
              {username.charAt(0).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
}
"""

# =======================
# LOGIN
# =======================
login_jsx = """
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Shield, KeyRound, User, Loader2, AlertCircle } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8080/api/login', { username, password });
      if (res.data.status === 'success') {
        localStorage.setItem('token', res.data.token);
        localStorage.setItem('role', res.data.role);
        localStorage.setItem('username', res.data.username);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Invalid credentials. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-slate-900 p-12 flex-col justify-between relative overflow-hidden">
        <div className="relative z-10">
          <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mb-8 shadow-xl shadow-blue-900/20">
            <Shield className="text-white w-8 h-8" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
            Employee Payroll<br/>Management System
          </h1>
          <p className="text-slate-400 text-lg max-w-md">
            Secure, centralized management for company payroll, personnel records, and access control.
          </p>
        </div>
        
        <div className="relative z-10">
          <p className="text-slate-500 text-sm font-medium">
            Internal Corporate System &copy; {new Date().getFullYear()}
          </p>
        </div>
        
        {/* Decorative background elements */}
        <div className="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 rounded-full bg-blue-600/10 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -ml-32 -mb-32 w-96 h-96 rounded-full bg-blue-400/5 blur-3xl"></div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Sign In</h2>
            <p className="mt-2 text-slate-500">Enter your credentials to access the system</p>
          </div>

          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-xl flex items-start space-x-3 border border-red-100">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <span className="text-sm font-medium leading-relaxed">{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700 block">Username</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                  <User size={18} />
                </div>
                <input
                  type="text"
                  required
                  className="w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition-all"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700 block">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                  <KeyRound size={18} />
                </div>
                <input
                  type="password"
                  required
                  className="w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition-all"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 focus:ring-4 focus:ring-blue-100 transition-all disabled:opacity-70 flex items-center justify-center space-x-2 shadow-sm"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <span>Sign In</span>}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
"""

# =======================
# DASHBOARD
# =======================
dashboard_jsx = """
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Banknote, ShieldAlert, ArrowRight, Activity, CircleDollarSign } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState({ employees: 0, payrollTotal: 0, users: 0 });
  const [loading, setLoading] = useState(true);
  const role = localStorage.getItem('role') || 'Unknown';
  const username = localStorage.getItem('username') || '';

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = { headers: { Authorization: `Bearer ${token}` } };
        
        // Fetch real metrics
        const [empRes, usersRes] = await Promise.all([
          axios.get('http://localhost:8080/api/employees', config).catch(() => ({ data: [] })),
          axios.get('http://localhost:8080/api/users', config).catch(() => ({ data: [] }))
        ]);
        
        const totalSalary = empRes.data.reduce((sum, e) => sum + (parseFloat(e.basicSalary) || 0), 0);
        
        setStats({
          employees: empRes.data.length,
          users: usersRes.data.length,
          payrollTotal: totalSalary
        });
      } catch (err) {
        console.error("Dashboard fetch error", err);
      }
      setLoading(false);
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Welcome back, {username}!</h2>
          <p className="text-slate-500 mt-1">Here is what's happening in EPMS today.</p>
        </div>
        <div className="bg-slate-50 px-5 py-3 rounded-xl border border-slate-100 flex items-center space-x-3">
          <Activity className="text-blue-600 w-5 h-5" />
          <span className="text-sm font-semibold text-slate-700">System Status: Operational</span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-start space-x-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <Users size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 mb-1">Total Employees</p>
            <h3 className="text-3xl font-bold text-slate-800">{stats.employees}</h3>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-start space-x-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
            <CircleDollarSign size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 mb-1">Total Base Payroll</p>
            <h3 className="text-3xl font-bold text-slate-800">${stats.payrollTotal.toLocaleString(undefined, {minimumFractionDigits: 2})}</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-start space-x-4">
          <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center shrink-0">
            <ShieldAlert size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 mb-1">Authorized Users</p>
            <h3 className="text-3xl font-bold text-slate-800">{stats.users}</h3>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-100 bg-slate-50/50">
          <h3 className="text-lg font-bold text-slate-800">Quick Actions</h3>
        </div>
        <div className="divide-y divide-slate-100">
          <Link to="/employees" className="flex items-center justify-between p-6 hover:bg-slate-50 transition-colors group">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center group-hover:bg-blue-100 group-hover:text-blue-600 transition-colors">
                <Users size={20} />
              </div>
              <div>
                <p className="font-semibold text-slate-800">Manage Employees</p>
                <p className="text-sm text-slate-500">View, add, or update employee records</p>
              </div>
            </div>
            <ArrowRight className="text-slate-400 group-hover:text-blue-600 transition-colors" />
          </Link>
          
          <Link to="/payroll" className="flex items-center justify-between p-6 hover:bg-slate-50 transition-colors group">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center group-hover:bg-emerald-100 group-hover:text-emerald-600 transition-colors">
                <Banknote size={20} />
              </div>
              <div>
                <p className="font-semibold text-slate-800">Process Payroll</p>
                <p className="text-sm text-slate-500">Review salaries, deductions, and issue payments</p>
              </div>
            </div>
            <ArrowRight className="text-slate-400 group-hover:text-emerald-600 transition-colors" />
          </Link>
        </div>
      </div>
    </div>
  );
}
"""

# =======================
# SETTINGS
# =======================
settings_jsx = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Save, Loader2, AlertCircle, CheckCircle } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({ hraPercent: 0, daPercent: 0, pfPercent: 0, taxPercent: 0 });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });
  
  const role = localStorage.getItem('role') || '';
  const canEdit = hasPermission(role, PERMISSIONS.SETTINGS_ADMIN);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:8080/api/settings', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setSettings(res.data);
      } catch (err) {
        console.error("Failed to load settings", err);
      }
      setLoading(false);
    };
    fetchSettings();
  }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 4000);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!canEdit) return;
    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8080/api/settings', settings, {
        headers: { Authorization: `Bearer ${token}` }
      });
      showToast('success', 'Settings updated successfully.');
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to update settings.');
    }
    setSaving(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-medium tracking-wide">{notification.msg}</span>
        </div>
      )}

      <div>
        <h2 className="text-2xl font-bold text-slate-800">System Settings</h2>
        <p className="text-slate-500 mt-1">Configure global application parameters and payroll rates.</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <form onSubmit={handleSave}>
          <div className="p-6 md:p-8 space-y-8">
            <section>
              <h3 className="text-lg font-bold text-slate-800 mb-4 border-b border-slate-100 pb-2">Payroll Configuration (Percentages)</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">HRA Percentage (%)</label>
                  <input type="number" step="0.1" required disabled={!canEdit} className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500" value={settings.hraPercent} onChange={e => setSettings({...settings, hraPercent: parseFloat(e.target.value)})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">DA Percentage (%)</label>
                  <input type="number" step="0.1" required disabled={!canEdit} className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500" value={settings.daPercent} onChange={e => setSettings({...settings, daPercent: parseFloat(e.target.value)})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">PF Percentage (%)</label>
                  <input type="number" step="0.1" required disabled={!canEdit} className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500" value={settings.pfPercent} onChange={e => setSettings({...settings, pfPercent: parseFloat(e.target.value)})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Tax Percentage (%)</label>
                  <input type="number" step="0.1" required disabled={!canEdit} className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500" value={settings.taxPercent} onChange={e => setSettings({...settings, taxPercent: parseFloat(e.target.value)})} />
                </div>
              </div>
            </section>
          </div>
          
          {canEdit && (
            <div className="bg-slate-50 p-6 border-t border-slate-200 flex justify-end">
              <button type="submit" disabled={saving} className="px-6 py-2.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center justify-center space-x-2 min-w-[140px]">
                {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <><Save size={18}/><span>Save Configuration</span></>}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
"""

write_file("frontend/src/utils/auth.js", auth_js)
write_file("frontend/src/App.jsx", app_jsx)
write_file("frontend/src/layouts/Layout.jsx", layout_jsx)
write_file("frontend/src/pages/Login.jsx", login_jsx)
write_file("frontend/src/pages/Dashboard.jsx", dashboard_jsx)
write_file("frontend/src/pages/Settings.jsx", settings_jsx)
delete_file("frontend/src/pages/Leaves.jsx")
delete_file("frontend/src/pages/Register.jsx")

print("Stage 1 complete.")
