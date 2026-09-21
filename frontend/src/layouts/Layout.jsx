import React from 'react';
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users as UsersIcon, 
  CreditCard, 
  Settings as SettingsIcon, 
  LogOut,
  ShieldAlert
} from 'lucide-react';
import { hasPermission, PERMISSIONS } from '../utils/auth';

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = localStorage.getItem('role') || 'Unknown';
  const username = localStorage.getItem('username') || 'User';

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Employees', path: '/employees', icon: UsersIcon },
    { name: 'Payroll', path: '/payroll', icon: CreditCard },
  ];

  // Users page is visible to all basic roles but functionality inside is restricted
  if (hasPermission(role, PERMISSIONS.USERS_VIEW)) {
    navItems.push({ name: 'User Management', path: '/users', icon: ShieldAlert });
  }
  
  navItems.push({ name: 'Settings', path: '/settings', icon: SettingsIcon });

  const currentPathName = navItems.find(i => i.path === location.pathname)?.name || 'EPMS';

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col transition-all duration-300 hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl leading-none">E</span>
            </div>
            <span className="text-white font-bold text-lg tracking-wide">EPMS</span>
          </div>
        </div>
        
        <nav className="flex-1 py-6 px-4 flex flex-col gap-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                    isActive 
                      ? 'bg-blue-600 text-white font-medium shadow-md shadow-blue-900/20' 
                      : 'hover:bg-slate-800 hover:text-white'
                  }`
                }
              >
                <Icon size={20} className="shrink-0" />
                <span className="truncate">{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-slate-800">
          <button 
            onClick={handleLogout}
            className="flex items-center space-x-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:bg-slate-800 hover:text-white transition-all duration-200"
          >
            <LogOut size={20} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0 z-10">
          <h1 className="text-xl font-bold text-slate-800 hidden sm:block">{currentPathName}</h1>
          
          <div className="flex items-center space-x-4 ml-auto">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-bold text-slate-800 leading-tight">{username}</p>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{role}</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold border border-blue-200 shrink-0">
              {username.charAt(0).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
}