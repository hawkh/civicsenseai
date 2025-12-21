import React from 'react';
import { User } from '../types.tsx';
import { Plus, ShieldCheck, MapPin, Activity } from 'lucide-react';
interface HomeScreenProps {
  user: User | null;
  onStartReport: () => void;
}

const HomeScreen: React.FC<HomeScreenProps> = ({ user, onStartReport }) => {
  return (
    <div className="h-full flex flex-col p-4 md:p-10 bg-[#F8FAFF] overflow-hidden">
      <header className="flex justify-between items-center shrink-0 mb-4 md:mb-8">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(99,102,241,0.5)]"></div>
          <h1 className="font-black text-base md:text-xl tracking-tighter text-indigo-900">CIVIC SENSE AI</h1>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-white rounded-full shadow-sm border border-indigo-50">
          <ShieldCheck size={12} className="text-emerald-500" />
          <span className="text-[8px] font-black text-slate-500 uppercase tracking-wider">Secured</span>
        </div>
      </header>

      <div className="flex-1 flex flex-col justify-center items-center text-center gap-6 md:gap-12 min-h-0">
        <div className="space-y-2 md:space-y-4">
          <div className="flex flex-wrap justify-center gap-1.5">
            {['Safety', 'Environment', 'Utility'].map(tag => (
              <span key={tag} className="px-3 py-1 bg-white text-indigo-600 text-[8px] font-black uppercase tracking-widest rounded-full shadow-sm border border-indigo-50">
                {tag}
              </span>
            ))}
          </div>
          <h2 className="text-4xl md:text-7xl font-black tracking-tighter text-slate-900 leading-[0.9]">
            See an<br/><span className="text-indigo-600 underline decoration-indigo-100 underline-offset-4 md:underline-offset-8">Issue?</span>
          </h2>
          <p className="text-slate-400 text-xs md:text-base max-w-[240px] md:max-w-[320px] mx-auto font-bold leading-tight">
            Report city problems in seconds with AI-powered routing.
          </p>
        </div>

        <button
          onClick={onStartReport}
          className="relative w-24 h-24 md:w-36 md:h-36 bg-indigo-600 text-white rounded-[2.5rem] md:rounded-[3.5rem] flex flex-col items-center justify-center shadow-2xl shadow-indigo-200 hover:bg-amber-500 hover:shadow-amber-200 transition-all duration-500 active:scale-90 group shrink-0"
        >
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          <Plus size={32} className="md:size-[40px] group-hover:rotate-180 transition-transform duration-700" />
          <span className="text-[9px] md:text-xs font-black uppercase tracking-[0.2em] mt-1 md:mt-2">Report</span>
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 shrink-0 mt-4">
        <div className="glass p-3 md:p-5 rounded-3xl flex flex-col gap-1 border border-indigo-50 neo-shadow">
          <Activity size={16} className="text-indigo-600" />
          <p className="text-[8px] md:text-[10px] text-slate-500 font-black uppercase tracking-tight leading-none">
            2.4k Fixed
          </p>
        </div>
        <div className="glass p-3 md:p-5 rounded-3xl flex flex-col gap-1 border border-amber-50 neo-shadow">
          <MapPin size={16} className="text-amber-600" />
          <p className="text-[8px] md:text-[10px] text-slate-500 font-black uppercase tracking-tight leading-none">
            Global Hub
          </p>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
