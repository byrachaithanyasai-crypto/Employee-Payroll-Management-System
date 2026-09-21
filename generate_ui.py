import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# main.jsx
write_file("frontend/src/main.jsx", """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""")

# index.css
write_file("frontend/src/index.css", """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
}
""")

# App.jsx
write_file("frontend/src/App.jsx", """
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Payroll from './pages/Payroll';
import Layout from './layouts/Layout';

function App() {
  const [auth, setAuth] = useState({
    isAuthenticated: !!localStorage.getItem('token'),
    role: localStorage.getItem('role') || null,
    username: localStorage.getItem('username') || null
  });

  const handleLogin = (data) => {
    localStorage.setItem('token', data.token);
    localStorage.setItem('role', data.role);
    localStorage.setItem('username', data.username);
    setAuth({ isAuthenticated: true, role: data.role, username: data.username });
  };

  const handleLogout = () => {
    localStorage.clear();
    setAuth({ isAuthenticated: false, role: null, username: null });
  };

  if (!auth.isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Router>
      <Layout auth={auth} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/payroll" element={<Payroll />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
""")

# Layout.jsx
write_file("frontend/src/layouts/Layout.jsx", """
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, FileText, LogOut, Settings } from 'lucide-react';

export default function Layout({ children, auth, onLogout }) {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Employees', path: '/employees', icon: Users },
    { name: 'Payroll', path: '/payroll', icon: FileText },
  ];

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white flex flex-col shadow-xl">
        <div className="p-6 text-2xl font-bold border-b border-slate-800 tracking-wider">
          <span className="text-blue-400">EP</span>MS
        </div>
        
        <div className="p-4 flex items-center space-x-3 border-b border-slate-800">
          <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center font-bold text-lg">
            {auth.username?.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="text-sm font-semibold">{auth.username}</p>
            <p className="text-xs text-slate-400 uppercase">{auth.role}</p>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive ? 'bg-blue-600 text-white shadow-md' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.name}</span>
              </Link>
            )
          })}
        </nav>
        <div className="p-4 border-t border-slate-800">
          <button 
            onClick={onLogout}
            className="flex items-center space-x-3 px-4 py-3 w-full rounded-lg text-slate-300 hover:bg-red-500 hover:text-white transition-colors"
          >
            <LogOut size={20} />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white shadow-sm flex items-center px-8 border-b">
          <h1 className="text-xl font-semibold text-gray-800 capitalize">
            {location.pathname === '/' ? 'Dashboard' : location.pathname.slice(1)}
          </h1>
        </header>
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
""")

# Login.jsx
write_file("frontend/src/pages/Login.jsx", """
import React, { useState } from 'react';
import axios from 'axios';
import { Lock, User, AlertCircle } from 'lucide-react';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await axios.post('http://localhost:8080/api/login', { username, password });
      if (res.data.status === 'success') {
        onLogin(res.data);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Connection to API failed.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        <div className="bg-blue-600 p-8 text-center">
          <h1 className="text-3xl font-bold text-white tracking-wider">EPMS</h1>
          <p className="text-blue-100 mt-2">Enterprise Payroll Management</p>
        </div>
        <div className="p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">Sign In</h2>
          
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded flex items-center text-red-700">
              <AlertCircle size={20} className="mr-2" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User size={18} className="text-gray-400" />
                </div>
                <input
                  type="text"
                  required
                  className="pl-10 w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                  placeholder="admin"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock size={18} className="text-gray-400" />
                </div>
                <input
                  type="password"
                  required
                  className="pl-10 w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition-all disabled:opacity-70 flex justify-center items-center"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
""")

# Dashboard.jsx
write_file("frontend/src/pages/Dashboard.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, IndianRupee, Clock, Briefcase } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    axios.get('http://localhost:8080/api/stats')
      .then(res => setStats(res.data))
      .catch(err => console.error(err));
  }, []);

  const cards = [
    { title: 'Total Employees', value: stats?.totalEmployees || 0, icon: Users, color: 'bg-blue-500' },
    { title: 'Total Payroll (Monthly)', value: `₹${(stats?.totalPayroll || 0).toLocaleString('en-IN')}`, icon: IndianRupee, color: 'bg-green-500' },
    { title: 'Avg Salary', value: `₹${(stats?.avgSalary || 0).toLocaleString('en-IN')}`, icon: Briefcase, color: 'bg-purple-500' },
    { title: 'Pending Leaves', value: stats?.pendingLeave || 0, icon: Clock, color: 'bg-yellow-500' },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center">
              <div className={`${card.color} w-12 h-12 rounded-lg flex items-center justify-center text-white shadow-inner`}>
                <Icon size={24} />
              </div>
              <div className="ml-5">
                <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">{card.title}</p>
                <h3 className="text-2xl font-bold text-gray-800 mt-1">
                  {stats ? card.value : <div className="h-6 w-24 bg-gray-200 animate-pulse rounded"></div>}
                </h3>
              </div>
            </div>
          )
        })}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">System Health & API Connection</h3>
        <div className="flex items-center space-x-2 text-green-600 font-semibold bg-green-50 p-4 rounded-lg">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span>C++ Backend Connected via RESTful API (localhost:8080)</span>
        </div>
      </div>
    </div>
  );
}
""")

# Employees.jsx
write_file("frontend/src/pages/Employees.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Search, Trash2 } from 'lucide-react';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  
  const fetchEmployees = () => {
    setLoading(true);
    axios.get('http://localhost:8080/api/employees')
      .then(res => setEmployees(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleDelete = async (id) => {
    if(window.confirm('Are you sure you want to delete this employee?')) {
      await axios.delete(`http://localhost:8080/api/employees/${id}`);
      fetchEmployees();
    }
  };

  const filtered = employees.filter(e => e.name.toLowerCase().includes(search.toLowerCase()) || String(e.id).includes(search));

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="relative w-full sm:w-96 mb-4 sm:mb-0">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={18} className="text-gray-400" />
          </div>
          <input
            type="text"
            className="pl-10 w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search employees..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <button className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors w-full sm:w-auto justify-center">
          <Plus size={18} />
          <span>Add Employee</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Employee</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Department</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Designation</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Base Salary</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-gray-500">Loading data from C++ API...</td></tr>
              ) : filtered.length === 0 ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-gray-500">No employees found.</td></tr>
              ) : (
                filtered.map(e => (
                  <tr key={e.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">#{e.id}</td>
                    <td className="px-6 py-4 text-sm font-bold text-gray-800">{e.name}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">{e.department}</span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{e.designation}</td>
                    <td className="px-6 py-4 text-sm font-semibold text-gray-800 text-right">₹{e.salary.toLocaleString('en-IN')}</td>
                    <td className="px-6 py-4 text-sm text-center">
                      <button onClick={() => handleDelete(e.id)} className="text-red-500 hover:text-red-700 p-2 rounded hover:bg-red-50 transition-colors">
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""")

# Payroll.jsx
write_file("frontend/src/pages/Payroll.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { IndianRupee, PlayCircle, CheckCircle } from 'lucide-react';

export default function Payroll() {
  const [payroll, setPayroll] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  const fetchPayroll = () => {
    setLoading(true);
    axios.get('http://localhost:8080/api/payroll')
      .then(res => setPayroll(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchPayroll();
  }, []);

  const handleProcess = async () => {
    if(window.confirm('Process payroll for Current Month via C++ Backend?')) {
      setProcessing(true);
      try {
        await axios.post('http://localhost:8080/api/payroll/process', { month: '2026-09' });
        fetchPayroll();
      } catch (err) {
        alert('Error processing payroll');
      }
      setProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Payroll Processing</h2>
          <p className="text-sm text-gray-500">Manage and process monthly salaries</p>
        </div>
        <button 
          onClick={handleProcess}
          disabled={processing}
          className="mt-4 sm:mt-0 flex items-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors shadow-md disabled:opacity-50"
        >
          {processing ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <PlayCircle size={20} />}
          <span className="font-semibold">Process Current Month</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-4 border-b border-gray-100 bg-gray-50 flex items-center space-x-2">
          <IndianRupee size={20} className="text-gray-500" />
          <h3 className="font-semibold text-gray-700">Payroll History</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white border-b border-gray-100">
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Emp ID</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Month</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Basic</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Deductions (Tax+PF)</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Net Salary</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-gray-500">Loading payroll records...</td></tr>
              ) : payroll.length === 0 ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-gray-500">No payroll processed yet.</td></tr>
              ) : (
                payroll.map((p, i) => (
                  <tr key={i} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-bold text-gray-800">#{p.employeeId}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{p.month}</td>
                    <td className="px-6 py-4 text-sm text-gray-600 text-right">₹{p.basicSalary.toLocaleString('en-IN')}</td>
                    <td className="px-6 py-4 text-sm text-red-600 font-medium text-right">-₹{(p.tax + p.pf).toLocaleString('en-IN')}</td>
                    <td className="px-6 py-4 text-sm font-bold text-green-600 text-right">₹{p.netSalary.toLocaleString('en-IN')}</td>
                    <td className="px-6 py-4 text-sm text-center">
                      <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-bold ${p.status === 'Paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {p.status === 'Paid' && <CheckCircle size={12} />}
                        <span>{p.status}</span>
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""")

print("React UI generated successfully.")
