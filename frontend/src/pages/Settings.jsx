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
        const res = await axios.get('http://https://employee-payroll-management-system-lj0a.onrender.com/api/settings', {
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
      await axios.post('http://https://employee-payroll-management-system-lj0a.onrender.com/api/settings', settings, {
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