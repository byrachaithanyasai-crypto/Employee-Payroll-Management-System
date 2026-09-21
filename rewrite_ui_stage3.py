import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Wrote {path}")

users_jsx = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Shield, UserPlus, Trash2, Loader2, AlertCircle, CheckCircle, Search, ShieldCheck } from 'lucide-react';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({ username: '', password: '', role: 'Manager' });
  const [submitting, setSubmitting] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canManage = hasPermission(role, PERMISSIONS.USERS_MANAGE);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://localhost:8080/api/users', { headers: { Authorization: `Bearer ${token}` } });
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

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8080/api/users', formData, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'User account created successfully');
      setFormData({ username: '', password: '', role: 'Manager' });
      setShowAddForm(false);
      fetchUsers();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to create user');
    }
    setSubmitting(false);
  };

  const handleDelete = async (username) => {
    if (!window.confirm(`Delete user account '${username}'?`)) return;
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:8080/api/users/${username}`, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'User account deleted');
      fetchUsers();
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to delete user');
    }
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
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-purple-50 to-transparent rounded-bl-full pointer-events-none opacity-60"></div>
        <div className="relative z-10">
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Access Control</h2>
          <p className="text-slate-500 mt-1 text-sm font-medium">Manage system users and authorization roles.</p>
        </div>
        {canManage && !showAddForm && (
          <button onClick={() => setShowAddForm(true)} className="relative z-10 bg-purple-600 text-white px-5 py-2.5 rounded-xl font-bold hover:bg-purple-700 transition-all shadow-md shadow-purple-600/20 flex items-center space-x-2 shrink-0">
            <UserPlus size={18}/>
            <span>Create Account</span>
          </button>
        )}
      </div>

      {canManage && showAddForm && (
        <div className="bg-white rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden relative">
           <div className="absolute top-0 left-0 w-full h-1 bg-purple-500"></div>
           <div className="p-6 sm:p-8">
              <h3 className="text-lg font-extrabold text-slate-800 mb-6 flex items-center">
                <ShieldCheck className="w-5 h-5 mr-2 text-purple-600" />
                Provision New Access
              </h3>
              <form onSubmit={handleCreate} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Username</label>
                    <input type="text" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-600/20 focus:border-purple-600 outline-none transition-all font-medium text-slate-900" value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})} placeholder="e.g. jdoe_hr" />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Temporary Password</label>
                    <input type="password" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-600/20 focus:border-purple-600 outline-none transition-all font-medium text-slate-900" value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} placeholder="••••••••" />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-1.5">Authorization Role</label>
                    <select required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-600/20 focus:border-purple-600 outline-none transition-all bg-white font-medium text-slate-900" value={formData.role} onChange={e => setFormData({...formData, role: e.target.value})}>
                      <option value="Manager">Manager (Read-Only Users)</option>
                      <option value="HR">HR (Personnel & Payroll)</option>
                    </select>
                  </div>
                </div>
                <div className="flex justify-end space-x-3 pt-2">
                  <button type="button" onClick={() => setShowAddForm(false)} className="px-5 py-2.5 border border-slate-200 bg-white rounded-xl font-bold text-slate-600 hover:bg-slate-50 hover:text-slate-800 transition-colors shadow-sm">Cancel</button>
                  <button type="submit" disabled={submitting} className="px-6 py-2.5 bg-purple-600 text-white rounded-xl font-bold hover:bg-purple-700 transition-colors shadow-md shadow-purple-600/20 disabled:opacity-70 flex items-center">
                    {submitting ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : null}
                    {submitting ? 'Provisioning...' : 'Provision Account'}
                  </button>
                </div>
              </form>
           </div>
        </div>
      )}

      {/* Users Grid */}
      <div className="bg-white rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <h3 className="font-bold text-slate-800">Active Directory</h3>
          <span className="text-xs font-bold bg-slate-200 text-slate-600 px-2.5 py-1 rounded-full">{users.length} Users</span>
        </div>
        
        {loading ? (
          <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-purple-600" /></div>
        ) : users.length === 0 ? (
          <div className="text-center py-20 px-4">
            <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-5 border border-slate-100 shadow-inner">
              <Shield className="text-slate-400 w-10 h-10" />
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-1">No user accounts</h3>
            <p className="text-slate-500 font-medium text-sm">Provision users to grant access to the system.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6">
            {users.map(u => (
              <div key={u.username} className="bg-white border border-slate-200 rounded-2xl p-5 hover:border-purple-200 hover:shadow-lg hover:shadow-purple-900/5 transition-all group relative">
                <div className="flex justify-between items-start mb-4">
                  <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
                    <span className="text-lg font-bold text-slate-600 uppercase">{u.username.substring(0,2)}</span>
                  </div>
                  {canManage && (
                    <button onClick={() => handleDelete(u.username)} className="text-slate-300 hover:text-red-500 bg-white hover:bg-red-50 p-1.5 rounded-lg transition-colors border border-transparent hover:border-red-100">
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>
                <div>
                  <h4 className="font-extrabold text-slate-800 truncate" title={u.username}>{u.username}</h4>
                  <div className="mt-2 flex items-center">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider border ${
                        u.role === 'ADMIN' ? 'bg-red-50 text-red-700 border-red-200' :
                        u.role === 'HR' ? 'bg-purple-50 text-purple-700 border-purple-200' :
                        'bg-blue-50 text-blue-700 border-blue-200'
                    }`}>
                      {u.role}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
"""

settings_jsx = """
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { hasPermission, PERMISSIONS } from '../utils/auth';
import { Settings as SettingsIcon, Save, Loader2, CheckCircle, AlertCircle, Percent, Sliders } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({ hraPercent: 0, daPercent: 0, pfPercent: 0, taxPercent: 0 });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notification, setNotification] = useState({ show: false, type: '', msg: '' });

  const role = localStorage.getItem('role') || '';
  const canEdit = hasPermission(role, PERMISSIONS.SETTINGS_MANAGE);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:8080/api/settings', { headers: { Authorization: `Bearer ${token}` } });
        setSettings(res.data);
      } catch (err) {
        console.error(err);
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
    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8080/api/settings', settings, { headers: { Authorization: `Bearer ${token}` } });
      showToast('success', 'Configuration updated successfully');
    } catch (err) {
      showToast('error', err.response?.data?.message || 'Failed to update settings');
    }
    setSaving(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center p-20">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {notification.show && (
        <div className={`fixed top-6 right-6 z-50 p-4 rounded-xl shadow-xl flex items-center space-x-3 text-white transition-all ${notification.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'}`}>
          {notification.type === 'success' ? <CheckCircle size={20}/> : <AlertCircle size={20}/>}
          <span className="font-semibold text-sm tracking-wide">{notification.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 sm:p-8 rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 gap-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-orange-50 to-transparent rounded-bl-full pointer-events-none opacity-60"></div>
        <div className="relative z-10 flex items-center">
          <div className="w-12 h-12 bg-orange-100 text-orange-600 rounded-xl flex items-center justify-center mr-4 shadow-inner">
            <Sliders className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">System Configuration</h2>
            <p className="text-slate-500 mt-1 text-sm font-medium">Manage global payroll variables and taxation rates.</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-[0_2px_12px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden relative">
        <div className="px-8 py-6 border-b border-slate-100 bg-slate-50/50">
          <h3 className="text-lg font-bold text-slate-800">Payroll Calculation Rates</h3>
          <p className="text-slate-500 text-sm mt-1">These percentages are applied to the base salary during payroll processing.</p>
        </div>
        
        <form onSubmit={handleSave} className="p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            {/* HRA */}
            <div className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100 hover:border-blue-200 hover:shadow-md transition-all">
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-extrabold text-slate-700">House Rent Allowance (HRA)</label>
                <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center"><Percent size={14}/></div>
              </div>
              <div className="relative">
                <input 
                  type="number" step="0.01" required disabled={!canEdit}
                  className="w-full text-2xl font-bold px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500 text-slate-900 pr-12"
                  value={settings.hraPercent} onChange={e => setSettings({...settings, hraPercent: parseFloat(e.target.value)})}
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-lg">%</span>
              </div>
            </div>

            {/* DA */}
            <div className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100 hover:border-emerald-200 hover:shadow-md transition-all">
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-extrabold text-slate-700">Dearness Allowance (DA)</label>
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center"><Percent size={14}/></div>
              </div>
              <div className="relative">
                <input 
                  type="number" step="0.01" required disabled={!canEdit}
                  className="w-full text-2xl font-bold px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-600/20 focus:border-emerald-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500 text-slate-900 pr-12"
                  value={settings.daPercent} onChange={e => setSettings({...settings, daPercent: parseFloat(e.target.value)})}
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-lg">%</span>
              </div>
            </div>

            {/* PF */}
            <div className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100 hover:border-orange-200 hover:shadow-md transition-all">
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-extrabold text-slate-700">Provident Fund (PF)</label>
                <div className="w-8 h-8 rounded-lg bg-orange-100 text-orange-600 flex items-center justify-center"><Percent size={14}/></div>
              </div>
              <div className="relative">
                <input 
                  type="number" step="0.01" required disabled={!canEdit}
                  className="w-full text-2xl font-bold px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-600/20 focus:border-orange-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500 text-slate-900 pr-12"
                  value={settings.pfPercent} onChange={e => setSettings({...settings, pfPercent: parseFloat(e.target.value)})}
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-lg">%</span>
              </div>
            </div>

            {/* TAX */}
            <div className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100 hover:border-red-200 hover:shadow-md transition-all">
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-extrabold text-slate-700">Income Tax (TAX)</label>
                <div className="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center"><Percent size={14}/></div>
              </div>
              <div className="relative">
                <input 
                  type="number" step="0.01" required disabled={!canEdit}
                  className="w-full text-2xl font-bold px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-red-600/20 focus:border-red-600 outline-none transition-all disabled:bg-slate-100 disabled:text-slate-500 text-slate-900 pr-12"
                  value={settings.taxPercent} onChange={e => setSettings({...settings, taxPercent: parseFloat(e.target.value)})}
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-lg">%</span>
              </div>
            </div>

          </div>

          {canEdit && (
            <div className="mt-8 pt-8 border-t border-slate-100 flex justify-end">
              <button type="submit" disabled={saving} className="px-8 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/20 disabled:opacity-70 flex items-center">
                {saving ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <Save className="w-5 h-5 mr-2" />}
                {saving ? 'Saving Config...' : 'Save Configuration'}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
"""

write_file("frontend/src/pages/Users.jsx", users_jsx)
write_file("frontend/src/pages/Settings.jsx", settings_jsx)

print("Stage 3 complete.")
