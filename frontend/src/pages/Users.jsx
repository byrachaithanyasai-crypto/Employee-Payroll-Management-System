import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Shield, Plus, Trash2, X, AlertCircle, CheckCircle, ShieldAlert, Loader2, UserPlus } from 'lucide-react';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newUser, setNewUser] = useState({ username: '', password: '', role: 'HR' });
  const [submitting, setSubmitting] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canAdd = hasPermission(role, PERMISSIONS.USERS_CREATE);
  const canDelete = hasPermission(role, PERMISSIONS.USERS_DELETE);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://https://employee-payroll-management-system-lj0a.onrender.com/api/users', { headers: { Authorization: `Bearer ${token}` } });
      setUsers(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const showToast = (type, msg) => {
    setNotification({ show: true, type, msg });
    setTimeout(() => setNotification({ show: false, type: '', msg: '' }), 4000);
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://https://employee-payroll-management-system-lj0a.onrender.com/api/users', newUser, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'User account created');
      setShowModal(false);
      setNewUser({ username: '', password: '', role: 'HR' });
      fetchUsers();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Creation failed');
    }
    setSubmitting(false);
  };

  const handleDelete = async (username) => {
    if (!window.confirm(`Delete user '${username}'? Employee records are not affected.`)) return;
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://https://employee-payroll-management-system-lj0a.onrender.com/api/users/${username}`, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'User deleted successfully');
      fetchUsers();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Deletion failed. Check permissions.');
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-medium tracking-wide">{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200 gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">User Management</h2>
          <p className="text-slate-500 mt-1 text-sm">Manage accounts and application access.</p>
        </div>
        {canAdd && (
          <button onClick={() => setShowModal(true)} className="bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-sm flex items-center space-x-2 shrink-0">
            <UserPlus size={18}/>
            <span>Create User Account</span>
          </button>
        )}
      </div>

      {/* Users List */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-blue-600" /></div>
        ) : users.length === 0 ? (
          <div className="text-center py-16 px-4">
            <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
              <ShieldAlert className="text-slate-400 w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No additional users</h3>
            <p className="text-slate-500">Only the built-in admin account exists.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6 bg-slate-50">
            {users.map(u => (
              <div key={u.username} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex items-center justify-between group hover:border-blue-200 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0 
                    ${u.role.toUpperCase() === 'HR' ? 'bg-purple-100 text-purple-700' : 'bg-emerald-100 text-emerald-700'}`}>
                    {u.role.toUpperCase() === 'HR' ? 'HR' : 'MGR'}
                  </div>
                  <div>
                    <p className="font-bold text-slate-800">{u.username}</p>
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{u.role}</p>
                  </div>
                </div>
                {canDelete && (
                  <button onClick={() => handleDelete(u.username)} className="p-2 text-slate-300 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100">
                    <Trash2 size={18} />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-40 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden flex flex-col">
            <div className="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50 shrink-0">
              <div>
                <h3 className="text-xl font-bold text-slate-800">Create Account</h3>
              </div>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 transition-colors bg-white rounded-full p-1 shadow-sm border border-slate-200"><X size={20}/></button>
            </div>
            
            <form onSubmit={handleCreateUser} className="flex flex-col">
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Username</label>
                  <input type="text" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={newUser.username} onChange={e => setNewUser({...newUser, username: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Password</label>
                  <input type="password" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Role</label>
                  <select required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none bg-white" value={newUser.role} onChange={e => setNewUser({...newUser, role: e.target.value})}>
                    <option value="HR">HR</option>
                    <option value="Manager">MANAGER</option>
                  </select>
                </div>
              </div>
              
              <div className="p-6 border-t border-slate-100 bg-slate-50 flex justify-end space-x-3 shrink-0">
                <button type="button" onClick={() => setShowModal(false)} className="px-5 py-2.5 border border-slate-200 rounded-xl font-semibold text-slate-600 hover:bg-white transition-colors">Cancel</button>
                <button type="submit" disabled={submitting} className="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center min-w-[120px] justify-center">
                  {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}