import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Wrote {path}")

app_jsx = """
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layouts/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Payroll from './pages/Payroll';
import Users from './pages/Users';
import Settings from './pages/Settings';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="employees" element={<Employees />} />
        <Route path="payroll" element={<Payroll />} />
        <Route path="users" element={<Users />} />
        <Route path="settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
"""

layout_jsx = """
import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, CreditCard, Shield, Settings, LogOut, Menu, X, ChevronRight, UserCircle } from 'lucide-react';

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = localStorage.getItem('role') || 'Unknown';
  const username = localStorage.getItem('username') || 'User';
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const navItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/employees', icon: Users, label: 'Employees' },
    { to: '/payroll', icon: CreditCard, label: 'Payroll' },
    { to: '/users', icon: Shield, label: 'Users' },
    { to: '/settings', icon: Settings, label: 'Settings' }
  ];

  const pageTitle = navItems.find(item => item.to === location.pathname)?.label || 'EPMS';

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-[#0f172a] text-slate-300 w-64 border-r border-slate-800 shrink-0">
      <div className="h-20 flex items-center px-6 mb-4">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-900/20 mr-3">
          <span className="text-white font-bold text-xl tracking-tight">EP</span>
        </div>
        <div>
          <h1 className="text-white font-bold text-lg tracking-tight leading-tight">Corporate</h1>
          <p className="text-blue-400 text-[10px] font-semibold uppercase tracking-widest">System</p>
        </div>
      </div>
      
      <div className="px-4 pb-6">
        <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-3 px-2">Main Menu</p>
        <nav className="space-y-1.5">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `flex items-center px-3 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 group ${
                  isActive 
                    ? 'bg-blue-600/10 text-blue-400' 
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <item.icon className={`w-5 h-5 mr-3 transition-colors ${isActive ? 'text-blue-500' : 'text-slate-500 group-hover:text-slate-300'}`} />
                  {item.label}
                  {isActive && <ChevronRight className="w-4 h-4 ml-auto text-blue-500 opacity-50" />}
                </>
              )}
            </NavLink>
          ))}
        </nav>
      </div>
      
      <div className="mt-auto p-4">
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center border border-slate-600 shrink-0">
              <UserCircle className="text-slate-300 w-6 h-6" />
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-bold text-white truncate">{username}</p>
              <p className="text-xs text-blue-400 font-semibold tracking-wide uppercase truncate">{role}</p>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-lg bg-slate-700/50 hover:bg-red-500/10 hover:text-red-400 text-slate-300 text-sm font-medium transition-colors border border-transparent hover:border-red-500/20"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-[#f8fafc] font-sans selection:bg-blue-100 selection:text-blue-900 overflow-hidden">
      
      {/* Desktop Sidebar */}
      <div className="hidden md:block shadow-2xl z-20">
        <SidebarContent />
      </div>

      {/* Mobile Sidebar Overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm" onClick={() => setMobileOpen(false)} />
          <div className="relative z-50 w-64 shadow-2xl transform transition-transform">
            <SidebarContent />
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        {/* Top Header */}
        <header className="h-20 bg-white border-b border-slate-200/60 flex items-center justify-between px-6 shrink-0 z-10 shadow-[0_4px_20px_-15px_rgba(0,0,0,0.05)]">
          <div className="flex items-center">
            <button onClick={() => setMobileOpen(true)} className="md:hidden p-2 mr-3 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
              <Menu className="w-6 h-6" />
            </button>
            <div>
              <h2 className="text-2xl font-bold text-slate-800 tracking-tight">{pageTitle}</h2>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center text-sm font-medium text-slate-500 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-100 shadow-sm">
              <div className="w-2 h-2 rounded-full bg-emerald-500 mr-2 shadow-[0_0_8px_rgba(16,185,129,0.6)]"></div>
              System Online
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-8 bg-[#f8fafc]">
          <div className="max-w-7xl mx-auto pb-12">
            <Outlet />
          </div>
        </main>

      </div>
    </div>
  );
}
"""

login_jsx = """
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Lock, User, ShieldCheck, Loader2 } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
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
      setError(err.response?.data?.message || 'Invalid credentials');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex bg-white font-sans">
      
      {/* Left Panel - Deep Navy / Brand */}
      <div className="hidden lg:flex lg:w-5/12 bg-[#0f172a] relative overflow-hidden flex-col justify-between p-12">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-600/20 to-transparent"></div>
        <div className="absolute -top-32 -left-32 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-32 -right-32 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl"></div>
        
        <div className="relative z-10">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-xl shadow-blue-900/30 mb-8 border border-blue-400/20">
            <ShieldCheck className="text-white w-8 h-8" />
          </div>
          <h1 className="text-4xl font-extrabold text-white tracking-tight leading-tight mb-4">
            Employee Payroll <br/>Management System
          </h1>
          <p className="text-slate-400 text-lg max-w-sm leading-relaxed">
            Enterprise-grade human resources and financial control platform.
          </p>
        </div>
        
        <div className="relative z-10">
          <p className="text-slate-500 text-sm font-medium">
            Chayy Corporate System &copy; {new Date().getFullYear()}
          </p>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 bg-slate-50 relative">
        <div className="mx-auto w-full max-w-md">
          
          <div className="text-center lg:text-left mb-10">
            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">Welcome back</h2>
            <p className="text-slate-500 font-medium text-sm">Please sign in to your secure account</p>
          </div>

          <div className="bg-white py-8 px-6 sm:px-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-2xl border border-slate-100">
            <form onSubmit={handleLogin} className="space-y-6">
              
              {error && (
                <div className="bg-red-50 border border-red-100 rounded-xl p-4 flex items-start space-x-3">
                  <AlertCircle className="text-red-600 w-5 h-5 shrink-0 mt-0.5" />
                  <p className="text-sm text-red-800 font-medium">{error}</p>
                </div>
              )}

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">Username</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                      <User className="h-5 w-5 text-slate-400" />
                    </div>
                    <input 
                      type="text" 
                      required 
                      className="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all bg-slate-50/50 focus:bg-white" 
                      placeholder="Enter your username"
                      value={username} 
                      onChange={e => setUsername(e.target.value)} 
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">Password</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-slate-400" />
                    </div>
                    <input 
                      type="password" 
                      required 
                      className="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all bg-slate-50/50 focus:bg-white" 
                      placeholder="••••••••"
                      value={password} 
                      onChange={e => setPassword(e.target.value)} 
                    />
                  </div>
                </div>
              </div>

              <div>
                <button 
                  type="submit" 
                  disabled={loading}
                  className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 transition-all disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Authenticating...</>
                  ) : (
                    'Sign In'
                  )}
                </button>
              </div>
              
            </form>
          </div>
          
          <div className="mt-8 text-center lg:hidden">
             <p className="text-slate-400 text-xs font-medium">Chayy Corporate System &copy; {new Date().getFullYear()}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

dashboard_jsx = """
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Banknote, ShieldAlert, Loader2, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:8080/api/stats', { headers: { Authorization: `Bearer ${token}` } });
        setStats(res.data);
      } catch (err) {
        setError('Failed to load dashboard data.');
      }
    };
    fetchStats();
  }, []);

  const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(val || 0);

  if (error) {
    return (
      <div className="bg-red-50 border border-red-100 rounded-2xl p-8 text-center max-w-lg mx-auto mt-10">
        <ShieldAlert className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-bold text-red-800 mb-2">Access Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600 mb-4" />
        <p className="text-slate-500 font-medium">Loading metrics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Card 1 */}
        <div className="bg-white rounded-2xl p-6 shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 relative overflow-hidden group hover:shadow-[0_8px_24px_rgb(0,0,0,0.06)] transition-all">
          <div className="absolute -right-6 -top-6 w-24 h-24 bg-blue-50 rounded-full group-hover:scale-150 transition-transform duration-500 ease-out z-0"></div>
          <div className="relative z-10 flex justify-between items-start">
            <div>
              <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Total Employees</p>
              <h3 className="text-4xl font-extrabold text-slate-800 tracking-tight">{stats.totalEmployees}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center shadow-inner">
              <Users className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Card 2 */}
        <div className="bg-white rounded-2xl p-6 shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 relative overflow-hidden group hover:shadow-[0_8px_24px_rgb(0,0,0,0.06)] transition-all">
          <div className="absolute -right-6 -top-6 w-24 h-24 bg-emerald-50 rounded-full group-hover:scale-150 transition-transform duration-500 ease-out z-0"></div>
          <div className="relative z-10 flex justify-between items-start">
            <div>
              <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Total Payroll Base</p>
              <h3 className="text-3xl font-extrabold text-slate-800 tracking-tight mt-1">{formatCurrency(stats.totalPayroll)}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center shadow-inner">
              <Banknote className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Card 3 */}
        <div className="bg-white rounded-2xl p-6 shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 relative overflow-hidden group hover:shadow-[0_8px_24px_rgb(0,0,0,0.06)] transition-all lg:col-span-1 md:col-span-2">
          <div className="absolute -right-6 -top-6 w-24 h-24 bg-indigo-50 rounded-full group-hover:scale-150 transition-transform duration-500 ease-out z-0"></div>
          <div className="relative z-10 flex justify-between items-start">
            <div>
              <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Average Salary</p>
              <h3 className="text-3xl font-extrabold text-slate-800 tracking-tight mt-1">{formatCurrency(stats.avgSalary)}</h3>
            </div>
            <div className="w-12 h-12 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center shadow-inner">
              <Banknote className="w-6 h-6" />
            </div>
          </div>
        </div>

      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-2xl p-8 shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100">
        <h3 className="text-lg font-bold text-slate-800 tracking-tight mb-6 flex items-center">
          Quick Navigation
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button onClick={() => navigate('/employees')} className="text-left px-5 py-4 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 transition-all group">
            <p className="font-bold text-slate-800 group-hover:text-blue-700">View Employees</p>
            <p className="text-xs text-slate-500 mt-1">Manage personnel records</p>
          </button>
          <button onClick={() => navigate('/payroll')} className="text-left px-5 py-4 rounded-xl border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 transition-all group">
            <p className="font-bold text-slate-800 group-hover:text-emerald-700">Review Payroll</p>
            <p className="text-xs text-slate-500 mt-1">Process and review salaries</p>
          </button>
          <button onClick={() => navigate('/users')} className="text-left px-5 py-4 rounded-xl border border-slate-200 hover:border-purple-300 hover:bg-purple-50/50 transition-all group">
            <p className="font-bold text-slate-800 group-hover:text-purple-700">System Users</p>
            <p className="text-xs text-slate-500 mt-1">Manage access control</p>
          </button>
          <button onClick={() => navigate('/settings')} className="text-left px-5 py-4 rounded-xl border border-slate-200 hover:border-orange-300 hover:bg-orange-50/50 transition-all group">
            <p className="font-bold text-slate-800 group-hover:text-orange-700">Configuration</p>
            <p className="text-xs text-slate-500 mt-1">Adjust payroll percentages</p>
          </button>
        </div>
      </div>

    </div>
  );
}
"""

write_file("frontend/src/App.jsx", app_jsx)
write_file("frontend/src/layouts/Layout.jsx", layout_jsx)
write_file("frontend/src/pages/Login.jsx", login_jsx)
write_file("frontend/src/pages/Dashboard.jsx", dashboard_jsx)

print("Stage 1 complete.")
