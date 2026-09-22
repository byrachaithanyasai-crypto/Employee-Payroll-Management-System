import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Users as UsersIcon,
  CreditCard,
  Settings as SettingsIcon,
  LogOut,
  ShieldAlert,
  Menu,
  X
} from 'lucide-react';
import { hasPermission, PERMISSIONS } from '../utils/auth';

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const role = localStorage.getItem('role') || 'Unknown';
  const username = localStorage.getItem('username') || 'User';
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Employees', path: '/employees', icon: UsersIcon },
    { name: 'Payroll', path: '/payroll', icon: CreditCard },
  ];

  if (hasPermission(role, PERMISSIONS.USERS_VIEW)) {
    navItems.push({ name: 'User Management', path: '/users', icon: ShieldAlert });
  }

  navItems.push({ name: 'Settings', path: '/settings', icon: SettingsIcon });

  const currentPathName = navItems.find(i => i.path === location.pathname)?.name || 'EPMS';

  const SidebarContent = () => (
    <>
      <div className="h-16 flex items-center justify-between px-6 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl leading-none">E</span>
          </div>
          <span className="text-white font-bold text-lg tracking-wide">EPMS</span>
        </div>
        <button className="md:hidden text-slate-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
          <X size={24} />
        </button>
      </div>

      <nav className="flex-1 py-6 px-4 flex flex-col gap-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setMobileMenuOpen(false)}
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
        <div className="flex items-center px-4 py-2 mb-4 md:hidden">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold border border-blue-200 shrink-0 mr-3">
              {username.charAt(0).toUpperCase()}
            </div>
            <div className="text-left">
              <p className="text-sm font-bold text-slate-300 leading-tight">{username}</p>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{role}</p>
            </div>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center space-x-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:bg-slate-800 hover:text-white transition-all duration-200"
        >
          <LogOut size={20} />
          <span>Sign Out</span>
        </button>
      </div>
    </>
  );

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 relative">
      {/* Mobile Overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed md:static inset-y-0 left-0 z-50 w-64 bg-slate-900 text-slate-300 flex flex-col transition-transform duration-300 ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <SidebarContent />
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden w-full">
        {/* Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 sm:px-6 shrink-0 z-10 w-full">
          <div className="flex items-center">
            <button
              className="md:hidden mr-4 text-slate-600 hover:text-slate-900 focus:outline-none"
              onClick={() => setMobileMenuOpen(true)}
            >
              <Menu size={24} />
            </button>
            <h1 className="text-lg sm:text-xl font-bold text-slate-800 truncate max-w-[150px] sm:max-w-xs">{currentPathName}</h1>
          </div>

          <div className="flex items-center space-x-3 sm:space-x-4 ml-auto">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-bold text-slate-800 leading-tight">{username}</p>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{role}</p>
            </div>
            <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold border border-blue-200 shrink-0">
              {username.charAt(0).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto w-full">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
}
