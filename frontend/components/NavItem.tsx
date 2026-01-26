import React from 'react';

interface NavItemProps {
  icon: any;
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const NavItem: React.FC<NavItemProps> = React.memo(({ icon: Icon, label, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
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
