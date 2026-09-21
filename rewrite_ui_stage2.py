import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Wrote {path}")

employees_jsx = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Users, Plus, Pencil, Trash2, X, Loader2, AlertCircle, CheckCircle, Search, UserPlus } from 'lucide-react';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({ id: '', name: '', department: '', designation: 'Developer', basicSalary: '' });
  const [submitting, setSubmitting] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canEdit = hasPermission(role, PERMISSIONS.EMPLOYEES_EDIT);
  const canDelete = hasPermission(role, PERMISSIONS.EMPLOYEES_DELETE);

  const fetchEmployees = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://localhost:8080/api/employees', { headers: { Authorization: `Bearer ${token}` } });
      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 4000);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const payload = {
        id: parseInt(formData.id),
        name: formData.name,
        department: formData.department,
        designation: formData.designation,
        basicSalary: parseFloat(formData.basicSalary)
      };

      if (editMode) {
        await axios.put(`http://localhost:8080/api/employees/${payload.id}`, payload, { headers: { Authorization: `Bearer ${token}` } });
        showToast('success', 'Employee updated successfully');
      } else {
        await axios.post('http://localhost:8080/api/employees', payload, { headers: { Authorization: `Bearer ${token}` } });
        showToast('success', 'Employee created successfully');
      }
      setShowModal(false);
      fetchEmployees();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to save employee');
    }
    setSubmitting(false);
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Delete employee ${name} (${id})?`)) return;
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:8080/api/employees/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'Employee deleted');
      fetchEmployees();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to delete');
    }
  };

  const openAddModal = () => {
    setEditMode(false);
    setFormData({ id: '', name: '', department: '', designation: 'Developer', basicSalary: '' });
    setShowModal(true);
  };

  const openEditModal = (emp) => {
    setEditMode(true);
    setFormData({ id: emp.id, name: emp.name, department: emp.department, designation: emp.designation, basicSalary: emp.basicSalary });
    setShowModal(true);
  };

  return (
    <div className="space-y-6">
      {notification.show && (
        <div className={`fixed top-6 right-6 z-50 p-4 rounded-xl shadow-xl flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-semibold text-sm tracking-wide">{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 sm:p-8 rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 gap-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-50 to-transparent rounded-bl-full pointer-events-none opacity-60"></div>
        <div className="relative z-10">
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Personnel Directory</h2>
          <p className="text-slate-500 mt-1 text-sm font-medium">Manage employee records and profiles.</p>
        </div>
        {canEdit && (
          <button onClick={openAddModal} className="relative z-10 bg-blue-600 text-white px-5 py-2.5 rounded-xl font-bold hover:bg-blue-700 transition-all shadow-md shadow-blue-600/20 flex items-center space-x-2 shrink-0">
            <UserPlus size={18}/>
            <span>Add Employee</span>
          </button>
        )}
      </div>

      {/* Table Section */}
      <div className="bg-white rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>
        ) : employees.length === 0 ? (
          <div className="text-center py-20 px-4">
            <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-5 border border-slate-100 shadow-inner">
              <Users className="text-slate-400 w-10 h-10" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No employees found</h3>
            <p className="text-slate-500 font-medium text-sm">Add your first employee to get started.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/80 border-b border-slate-200">
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">ID</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">Employee</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">Department</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">Designation</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Base Salary</th>
                  {(canEdit || canDelete) && <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {employees.map(emp => (
                  <tr key={emp.id} className="hover:bg-slate-50/50 transition-colors group">
                    <td className="py-4 px-6 font-semibold text-slate-500 text-sm">#{emp.id}</td>
                    <td className="py-4 px-6">
                      <div className="font-bold text-slate-900">{emp.name}</div>
                    </td>
                    <td className="py-4 px-6">
                      <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-slate-100 text-slate-600 border border-slate-200">
                        {emp.department}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold border ${
                        emp.designation.toUpperCase() === 'MANAGER' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' :
                        emp.designation.toUpperCase() === 'HR' ? 'bg-purple-50 text-purple-700 border-purple-200' :
                        'bg-blue-50 text-blue-700 border-blue-200'
                      }`}>
                        {emp.designation}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-right font-bold text-slate-700 tabular-nums">
                      ${emp.basicSalary.toLocaleString()}
                    </td>
                    {(canEdit || canDelete) && (
                      <td className="py-4 px-6 text-right">
                        <div className="flex justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          {canEdit && (
                            <button onClick={() => openEditModal(emp)} className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                              <Pencil size={18} />
                            </button>
                          )}
                          {canDelete && (
                            <button onClick={() => handleDelete(emp.id, emp.name)} className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                              <Trash2 size={18} />
                            </button>
                          )}
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden flex flex-col transform transition-all">
            <div className="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50/80">
              <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">{editMode ? 'Edit Employee' : 'Add New Employee'}</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 transition-colors bg-white rounded-full p-1.5 shadow-sm border border-slate-200"><X size={20}/></button>
            </div>
            
            <form onSubmit={handleSave} className="flex flex-col">
              <div className="p-6 space-y-5">
                <div className="grid grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Employee ID</label>
                    <input type="number" required disabled={editMode} className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all disabled:bg-slate-50 disabled:text-slate-500 font-medium" value={formData.id} onChange={e => setFormData({...formData, id: e.target.value})} />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Full Name</label>
                    <input type="text" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all font-medium text-slate-900" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Department</label>
                    <input type="text" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all font-medium text-slate-900" value={formData.department} onChange={e => setFormData({...formData, department: e.target.value})} />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Designation / Role</label>
                    <select required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all bg-white font-medium text-slate-900" value={formData.designation} onChange={e => setFormData({...formData, designation: e.target.value})}>
                      <option value="Developer">Developer</option>
                      <option value="HR">HR</option>
                      <option value="Manager">Manager</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-1.5">Base Salary (USD)</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">$</span>
                    <input type="number" required step="0.01" className="w-full pl-9 pr-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all font-bold text-slate-900" value={formData.basicSalary} onChange={e => setFormData({...formData, basicSalary: e.target.value})} />
                  </div>
                </div>
              </div>
              
              <div className="p-6 border-t border-slate-100 bg-slate-50/80 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 border border-slate-200 bg-white rounded-xl font-bold text-slate-600 hover:bg-slate-50 hover:text-slate-800 transition-colors shadow-sm">Cancel</button>
                <button type="submit" disabled={submitting} className="px-6 py-2.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md shadow-blue-600/20 disabled:opacity-70 flex items-center min-w-[120px] justify-center">
                  {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Save Record'}
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

payroll_jsx = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Calculator, Loader2, CheckCircle, AlertCircle, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

export default function Payroll() {
  const [payrolls, setPayrolls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canProcess = hasPermission(role, PERMISSIONS.PAYROLL_PROCESS);

  const fetchPayroll = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://localhost:8080/api/payroll', { headers: { Authorization: `Bearer ${token}` } });
      setPayrolls(res.data);
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
    setProcessing(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8080/api/payroll/process', {}, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'Payroll calculated for current period');
      fetchPayroll();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to process payroll');
    }
    setProcessing(false);
  };

  const formatMoney = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);

  return (
    <div className="space-y-6">
      {notification.show && (
        <div className={`fixed top-6 right-6 z-50 p-4 rounded-xl shadow-xl flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-semibold text-sm tracking-wide">{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 sm:p-8 rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 gap-4 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-64 h-64 bg-gradient-to-br from-emerald-50 to-transparent rounded-br-full pointer-events-none opacity-60"></div>
        <div className="relative z-10">
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Payroll Processing</h2>
          <p className="text-slate-500 mt-1 text-sm font-medium">Review and process employee salaries.</p>
        </div>
        {canProcess && (
          <button onClick={handleProcessPayroll} disabled={processing} className="relative z-10 bg-emerald-600 text-white px-5 py-2.5 rounded-xl font-bold hover:bg-emerald-700 transition-all shadow-md shadow-emerald-600/20 flex items-center space-x-2 shrink-0 disabled:opacity-70">
            {processing ? <Loader2 size={18} className="animate-spin" /> : <Calculator size={18} />}
            <span>Process Current Period</span>
          </button>
        )}
      </div>

      {/* Data Grid */}
      <div className="bg-white rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-emerald-600" /></div>
        ) : payrolls.length === 0 ? (
          <div className="text-center py-20 px-4">
            <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-5 border border-slate-100 shadow-inner">
              <DollarSign className="text-slate-400 w-10 h-10" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No payroll records</h3>
            <p className="text-slate-500 font-medium text-sm">Process payroll to generate salary slips.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/80 border-b border-slate-200">
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">Employee ID</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider">Period</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Base Salary</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Earnings</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Deductions</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-800 uppercase tracking-wider text-right">Net Salary</th>
                  <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {payrolls.map((p, idx) => {
                  const earnings = p.hra + p.da;
                  const deductions = p.pf + p.tax;
                  return (
                    <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                      <td className="py-4 px-6 font-bold text-slate-700">#{p.employeeId}</td>
                      <td className="py-4 px-6 font-semibold text-slate-500 text-sm">{p.month}</td>
                      <td className="py-4 px-6 text-right font-medium text-slate-600 tabular-nums">{formatMoney(p.basicSalary)}</td>
                      <td className="py-4 px-6 text-right text-emerald-600 font-semibold tabular-nums flex items-center justify-end gap-1">
                        <TrendingUp size={14}/> {formatMoney(earnings)}
                      </td>
                      <td className="py-4 px-6 text-right text-red-500 font-semibold tabular-nums">
                        <span className="flex items-center justify-end gap-1"><TrendingDown size={14}/> {formatMoney(deductions)}</span>
                      </td>
                      <td className="py-4 px-6 text-right font-extrabold text-slate-900 tabular-nums bg-slate-50/50">
                        {formatMoney(p.netSalary)}
                      </td>
                      <td className="py-4 px-6 text-center">
                        <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold border ${
                          p.status === 'Paid' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-orange-50 text-orange-700 border-orange-200'
                        }`}>
                          {p.status}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
"""

write_file("frontend/src/pages/Employees.jsx", employees_jsx)
write_file("frontend/src/pages/Payroll.jsx", payroll_jsx)

print("Stage 2 complete.")
