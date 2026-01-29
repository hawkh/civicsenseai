import React, { memo } from 'react';
import { AppState } from '../types';

interface NavItemProps {
  page: AppState;
  isActive: boolean;
  onNavigate: (page: AppState) => void;
  icon: any;
  label: string;
}

// ⚡ Bolt Optimization: Wrapped in React.memo to prevent unnecessary re-renders
const NavItem: React.FC<NavItemProps> = memo(({ page, isActive, onNavigate, icon: Icon, label }) => {
  return (
    <button
      onClick={() => onNavigate(page)}
      className={`flex items-center gap-3 px-5 py-3 rounded-2xl transition-all duration-300 w-full ${
        isActive
          ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-200'
          : 'text-slate-400 hover:text-indigo-600 hover:bg-indigo-50'
      }`}
    >
      <Icon size={20} />
      <span className="text-sm font-bold tracking-tight">{label}</span>
    </button>
  );
});

export default NavItem;
