import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Plus, Search, User, Edit2, Trash2, X, AlertCircle, CheckCircle, Briefcase, Mail, Phone, DollarSign, Loader2 } from 'lucide-react';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState('add');
  const [currentEmp, setCurrentEmp] = useState({ id: 0, name: '', department: '', designation: '', basicSalary: 0 });
  const [submitting, setSubmitting] = useState(false);
  
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });
  
  const role = localStorage.getItem('role') || '';
  const canAdd = hasPermission(role, PERMISSIONS.EMPLOYEES_CREATE);
  const canEdit = hasPermission(role, PERMISSIONS.EMPLOYEES_EDIT);
  const canDelete = hasPermission(role, PERMISSIONS.EMPLOYEES_DELETE);

  const fetchEmployees = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('https://employee-payroll-management-system-lj0a.onrender.com/api/employees', { headers: { Authorization: `Bearer ${token}` } });
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
      const config = { headers: { Authorization: `Bearer ${token}` } };
      
      const payload = {
        id: parseInt(currentEmp.id),
        name: currentEmp.name,
        department: currentEmp.department,
        designation: currentEmp.designation,
        basicSalary: parseFloat(currentEmp.basicSalary)
      };

      if (modalMode === 'add') {
        await axios.post('https://employee-payroll-management-system-lj0a.onrender.com/api/employees', payload, config);
        showToast('success', 'Employee added successfully');
      } else {
        await axios.put(`https://employee-payroll-management-system-lj0a.onrender.com/api/employees/${currentEmp.id}`, payload, config);
        showToast('success', 'Employee updated successfully');
      }
      setShowModal(false);
      fetchEmployees();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Operation failed. Check permissions.');
    }
    setSubmitting(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this employee? This will also remove their payroll records.")) return;
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`https://employee-payroll-management-system-lj0a.onrender.com/api/employees/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'Employee deleted');
      fetchEmployees();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Deletion failed. Check permissions.');
    }
  };

  const filtered = employees.filter(e => 
    e.name.toLowerCase().includes(search.toLowerCase()) || 
    e.department.toLowerCase().includes(search.toLowerCase()) ||
    e.id.toString().includes(search)
  );

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
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Employees</h2>
          <p className="text-slate-500 mt-1 text-sm">Manage personnel records and information.</p>
        </div>
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <Search size={18} />
            </div>
            <input 
              type="text" 
              className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all bg-slate-50 focus:bg-white text-sm" 
              placeholder="Search employees..." 
              value={search} 
              onChange={e => setSearch(e.target.value)} 
            />
          </div>
          {canAdd && (
            <button onClick={() => { setModalMode('add'); setCurrentEmp({ id: '', name: '', department: '', designation: '', basicSalary: '' }); setShowModal(true); }} className="bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-sm flex items-center space-x-2 shrink-0">
              <Plus size={18}/>
              <span className="hidden sm:inline">Add Employee</span>
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 px-4">
            <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
              <User className="text-slate-400 w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No employees found</h3>
            <p className="text-slate-500">There are no employee records matching your criteria.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Employee</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Department</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Role</th>
                  <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Salary</th>
                  {(canEdit || canDelete) && <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map(emp => (
                  <tr key={emp.id} className="hover:bg-slate-50/50 transition-colors group">
                    <td className="px-6 py-4 text-sm font-semibold text-slate-700 whitespace-nowrap">#{emp.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs shrink-0">
                          {emp.name.charAt(0).toUpperCase()}
                        </div>
                        <span className="font-bold text-slate-800">{emp.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 whitespace-nowrap">{emp.department}</td>
                    <td className="px-6 py-4 text-sm text-slate-600 whitespace-nowrap">{emp.designation}</td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-800 whitespace-nowrap">
                      ${parseFloat(emp.basicSalary).toLocaleString(undefined, {minimumFractionDigits: 2})}
                    </td>
                    {(canEdit || canDelete) && (
                      <td className="px-6 py-4 whitespace-nowrap text-right space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        {canEdit && (
                          <button onClick={() => { setModalMode('edit'); setCurrentEmp(emp); setShowModal(true); }} className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                            <Edit2 size={16} />
                          </button>
                        )}
                        {canDelete && (
                          <button onClick={() => handleDelete(emp.id)} className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                            <Trash2 size={16} />
                          </button>
                        )}
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
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-40 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh]">
            <div className="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50 shrink-0">
              <div>
                <h3 className="text-xl font-bold text-slate-800">{modalMode === 'add' ? 'Add Employee' : 'Edit Employee'}</h3>
                <p className="text-xs text-slate-500 mt-1">Enter the personnel details below.</p>
              </div>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 transition-colors bg-white rounded-full p-1 shadow-sm border border-slate-200"><X size={20}/></button>
            </div>
            
            <form onSubmit={handleSave} className="flex flex-col overflow-hidden">
              <div className="p-6 space-y-5 overflow-y-auto">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Employee ID</label>
                    <input type="number" required disabled={modalMode === 'edit'} className="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none disabled:bg-slate-100" value={currentEmp.id} onChange={e => setCurrentEmp({...currentEmp, id: e.target.value})} />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Full Name</label>
                    <input type="text" required className="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={currentEmp.name} onChange={e => setCurrentEmp({...currentEmp, name: e.target.value})} />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Department</label>
                    <input type="text" required className="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={currentEmp.department} onChange={e => setCurrentEmp({...currentEmp, department: e.target.value})} />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1">Designation</label>
                    <input type="text" required className="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={currentEmp.designation} onChange={e => setCurrentEmp({...currentEmp, designation: e.target.value})} />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Basic Salary</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500"><DollarSign size={16}/></div>
                    <input type="number" step="0.01" required className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={currentEmp.basicSalary} onChange={e => setCurrentEmp({...currentEmp, basicSalary: e.target.value})} />
                  </div>
                </div>
              </div>
              
              <div className="p-6 border-t border-slate-100 bg-slate-50 flex justify-end space-x-3 shrink-0">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 border border-slate-200 rounded-xl font-semibold text-slate-600 hover:bg-white transition-colors">Cancel</button>
                <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center min-w-[120px] justify-center">
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