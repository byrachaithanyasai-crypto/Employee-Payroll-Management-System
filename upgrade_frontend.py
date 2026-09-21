import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write_file("frontend/src/pages/Register.jsx", """
import React, { useState } from 'react';
import axios from 'axios';
import { User, Lock, Mail, AlertCircle, ArrowLeft } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export default function Register() {
  const [formData, setFormData] = useState({ username: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(formData.password !== formData.confirm) return setError('Passwords do not match');
    setLoading(true); setError('');
    try {
      await axios.post('http://localhost:8080/api/register', formData);
      navigate('/login?registered=true');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        <div className="bg-slate-900 p-8 text-center border-b-4 border-blue-600">
          <h1 className="text-3xl font-bold text-white tracking-wider">EPMS</h1>
          <p className="text-blue-100 mt-2">Employee Payroll Management System</p>
        </div>
        <div className="p-8">
          <div className="flex items-center mb-6 text-gray-600">
            <Link to="/login" className="hover:text-blue-600 mr-3"><ArrowLeft size={20}/></Link>
            <h2 className="text-2xl font-semibold">Create Account</h2>
          </div>
          {error && (
            <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 flex items-center text-red-700 text-sm">
              <AlertCircle size={16} className="mr-2" />{error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <div className="relative">
                <User size={16} className="absolute left-3 top-3.5 text-gray-400" />
                <input type="text" required className="pl-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600" onChange={e => setFormData({...formData, username: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <div className="relative">
                <Mail size={16} className="absolute left-3 top-3.5 text-gray-400" />
                <input type="email" required className="pl-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600" onChange={e => setFormData({...formData, email: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-3 top-3.5 text-gray-400" />
                <input type="password" required className="pl-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600" onChange={e => setFormData({...formData, password: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-3 top-3.5 text-gray-400" />
                <input type="password" required className="pl-10 w-full px-4 py-3 bg-gray-50 border rounded-lg focus:ring-2 focus:ring-blue-600" onChange={e => setFormData({...formData, confirm: e.target.value})} />
              </div>
            </div>
            <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-all flex justify-center">
              {loading ? <div className="w-5 h-5 border-2 border-t-transparent rounded-full animate-spin"></div> : 'Register'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
""")

write_file("frontend/src/pages/Leaves.jsx", """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, Check, X } from 'lucide-react';

export default function Leaves() {
  const [leaves, setLeaves] = useState([]);
  
  const fetchLeaves = () => {
    axios.get('http://localhost:8080/api/leaves').then(res => setLeaves(res.data)).catch(console.error);
  };
  useEffect(fetchLeaves, []);

  const handleApprove = async (id) => {
    await axios.post(`http://localhost:8080/api/leaves/${id}/approve`);
    fetchLeaves();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border">
        <h2 className="text-xl font-bold text-slate-800">Leave Management</h2>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Apply Leave</button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b">
            <tr>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Emp ID</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Type</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Days</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Status</th>
              <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {leaves.map(l => (
              <tr key={l.id}>
                <td className="px-6 py-4 font-medium">#{l.employeeId}</td>
                <td className="px-6 py-4">{l.type}</td>
                <td className="px-6 py-4">{l.days} days</td>
                <td className="px-6 py-4"><span className={`px-2 py-1 text-xs rounded-full font-bold ${l.status==='APPROVED'?'bg-green-100 text-green-800':'bg-yellow-100 text-yellow-800'}`}>{l.status}</span></td>
                <td className="px-6 py-4 text-center">
                  {l.status === 'PENDING' && (
                    <button onClick={() => handleApprove(l.id)} className="text-green-600 hover:bg-green-50 p-2 rounded"><Check size={18}/></button>
                  )}
                </td>
              </tr>
            ))}
            {leaves.length === 0 && <tr><td colSpan="5" className="p-8 text-center text-slate-500">No leave requests found.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
""")

write_file("frontend/src/App.jsx", """
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Payroll from './pages/Payroll';
import Leaves from './pages/Leaves';
import Layout from './layouts/Layout';

export default function App() {
  const [auth, setAuth] = useState({ isAuthenticated: !!localStorage.getItem('token'), role: localStorage.getItem('role') || null, username: localStorage.getItem('username') || null });

  const handleLogin = (data) => {
    localStorage.setItem('token', data.token); localStorage.setItem('role', data.role); localStorage.setItem('username', data.username);
    setAuth({ isAuthenticated: true, role: data.role, username: data.username });
  };
  const handleLogout = () => { localStorage.clear(); setAuth({ isAuthenticated: false, role: null, username: null }); };

  return (
    <Router>
      {!auth.isAuthenticated ? (
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      ) : (
        <Layout auth={auth} onLogout={handleLogout}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/payroll" element={<Payroll />} />
            <Route path="/leaves" element={<Leaves />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Layout>
      )}
    </Router>
  );
}
""")

with open('frontend/src/pages/Login.jsx', 'r') as f:
    login_code = f.read()

login_code = login_code.replace("Enterprise Payroll Management", "Employee Payroll Management System")
login_code = login_code.replace("bg-blue-600 p-8", "bg-slate-900 p-8 border-b-4 border-blue-600")
login_code = login_code.replace("</form>", """
          </form>
          <div className="mt-6 text-center text-sm text-gray-500">
            Don't have an account? <Link to="/register" className="text-blue-600 font-semibold hover:underline">Create Account</Link>
          </div>
""")
login_code = "import { Link } from 'react-router-dom';\n" + login_code
write_file("frontend/src/pages/Login.jsx", login_code)

with open('frontend/src/layouts/Layout.jsx', 'r') as f:
    layout_code = f.read()

layout_code = "import { Calendar } from 'lucide-react';\n" + layout_code
layout_code = layout_code.replace("{ name: 'Payroll', path: '/payroll', icon: FileText },", "{ name: 'Payroll', path: '/payroll', icon: FileText },\n    { name: 'Leaves', path: '/leaves', icon: Calendar },")

write_file("frontend/src/layouts/Layout.jsx", layout_code)

print("Frontend React components upgraded!")
