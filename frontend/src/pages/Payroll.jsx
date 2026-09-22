import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Search, Calculator, CheckCircle, AlertCircle, FileText, Loader2 } from 'lucide-react';

export default function Payroll() {
  const [payroll, setPayroll] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [search, setSearch] = useState('');
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canProcess = hasPermission(role, PERMISSIONS.PAYROLL_PROCESS);

  const fetchPayroll = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://https://employee-payroll-management-system-lj0a.onrender.com/api/payroll', { headers: { Authorization: `Bearer ${token}` } });
      setPayroll(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPayroll();
  }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 4000);
  };

  const handleProcessPayroll = async () => {
    if (!window.confirm("Process payroll for all active employees?")) return;
    setProcessing(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://https://employee-payroll-management-system-lj0a.onrender.com/api/payroll/process', {}, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'Payroll processed successfully');
      fetchPayroll();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Processing failed. Check permissions.');
    }
    setProcessing(false);
  };

  const filtered = payroll.filter(p => p.employeeId.toString().includes(search));

  const totalBasic = filtered.reduce((acc, curr) => acc + (parseFloat(curr.basicSalary) || 0), 0);
  const totalNet = filtered.reduce((acc, curr) => acc + (parseFloat(curr.netSalary) || 0), 0);

  return (
    <div className="space-y-6">
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-medium tracking-wide">{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200 gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Payroll</h2>
          <p className="text-slate-500 mt-1 text-sm">Review employee salary disbursements.</p>
        </div>
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <Search size={18} />
            </div>
            <input type="text" className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none text-sm" placeholder="Search Employee ID..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          {canProcess && (
            <button onClick={handleProcessPayroll} disabled={processing} className="bg-emerald-600 text-white px-4 py-2 rounded-xl font-semibold hover:bg-emerald-700 transition-all shadow-sm flex items-center space-x-2 shrink-0 disabled:opacity-70">
              {processing ? <Loader2 size={18} className="animate-spin" /> : <Calculator size={18}/>}
              <span className="hidden sm:inline">Process Payroll</span>
            </button>
          )}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
          <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Filtered Basic Pay</p>
          <p className="text-2xl font-bold text-slate-800">${totalBasic.toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
        </div>
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
          <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Filtered Net Disbursed</p>
          <p className="text-2xl font-bold text-emerald-600">${totalNet.toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 px-4">
            <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
              <FileText className="text-slate-400 w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No payroll records found</h3>
            <p className="text-slate-500">Run 'Process Payroll' to generate records.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse min-w-[800px]">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">EMP ID</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Period</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Basic</th>
                  <th className="px-6 py-4 text-xs font-bold text-green-600 uppercase tracking-wider text-right">Earnings</th>
                  <th className="px-6 py-4 text-xs font-bold text-red-500 uppercase tracking-wider text-right">Deductions</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-800 uppercase tracking-wider text-right bg-slate-100">Net Salary</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map(p => {
                  const basic = parseFloat(p.basicSalary) || 0;
                  const earnings = (parseFloat(p.hra) || 0) + (parseFloat(p.da) || 0);
                  const deductions = (parseFloat(p.tax) || 0) + (parseFloat(p.pf) || 0);
                  const net = parseFloat(p.netSalary) || 0;

                  return (
                    <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-bold text-slate-800 whitespace-nowrap">#{p.employeeId}</td>
                      <td className="px-6 py-4 text-sm text-slate-600 whitespace-nowrap">{p.month} {p.year}</td>
                      <td className="px-6 py-4 text-sm font-medium text-slate-600 whitespace-nowrap text-right">${basic.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                      <td className="px-6 py-4 text-sm font-medium text-green-600 whitespace-nowrap text-right">+ ${earnings.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                      <td className="px-6 py-4 text-sm font-medium text-red-500 whitespace-nowrap text-right">- ${deductions.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                      <td className="px-6 py-4 text-sm font-bold text-slate-800 whitespace-nowrap text-right bg-slate-50/50">${net.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}