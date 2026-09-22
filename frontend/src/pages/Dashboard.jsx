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
          axios.get('http://https://employee-payroll-management-system-lj0a.onrender.com/api/employees', config).catch(() => ({ data: [] })),
          axios.get('http://https://employee-payroll-management-system-lj0a.onrender.com/api/users', config).catch(() => ({ data: [] }))
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