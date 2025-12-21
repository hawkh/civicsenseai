
import React from 'react';
import { User } from '../types.ts';
import { ShieldCheck, LogOut, Lock, Key, Fingerprint, RefreshCw, Zap, ShieldAlert } from 'lucide-react';

interface ProfileScreenProps {
  user: User | null;
  onLogout: () => void;
}

const ProfileScreen: React.FC<ProfileScreenProps> = ({ user, onLogout }) => {
  return (
    <div className="h-full bg-[#F8FAFF] p-4 md:p-10 flex flex-col items-center overflow-hidden">
      <div className="w-full max-w-md flex flex-col h-full gap-4 md:gap-8">
        
        {/* Profile Card */}
        <div className="bg-white rounded-[2.5rem] p-6 text-center shadow-xl shadow-indigo-100/50 border border-indigo-50 flex flex-col items-center gap-4 shrink-0">
          <div className="relative">
            <div className="w-20 h-20 bg-indigo-600 rounded-[2rem] flex items-center justify-center text-white shadow-2xl shadow-indigo-200 float">
              <Fingerprint size={32} strokeWidth={1.5} />
            </div>
            <div className="absolute -bottom-1 -right-1 bg-emerald-500 text-white p-1.5 rounded-xl border-2 border-white">
              <ShieldCheck size={14} />
            </div>
          </div>
          
          <div className="space-y-1">
            <h2 className="text-xl font-black text-slate-900 uppercase tracking-tighter">Verified Citizen</h2>
            <p className="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Node #{user?.id.substr(-6).toUpperCase()}</p>
          </div>

          <div className="flex gap-2">
            <span className="px-3 py-1 bg-emerald-50 text-emerald-600 text-[8px] font-black uppercase tracking-widest rounded-full border border-emerald-100">
              Identity Locked
            </span>
            <span className="px-3 py-1 bg-indigo-50 text-indigo-600 text-[8px] font-black uppercase tracking-widest rounded-full border border-indigo-100">
              Active Session
            </span>
          </div>
        </div>

        {/* Technical Hub */}
        <div className="flex-1 flex flex-col gap-4 min-h-0 overflow-hidden">
          <div className="flex items-center gap-3 px-2">
            <ShieldAlert size={14} className="text-amber-500" />
            <span className="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em]">Security Protocol</span>
          </div>

          <div className="flex-1 bg-white border border-indigo-50 rounded-[2.5rem] p-5 shadow-inner flex flex-col justify-around min-h-0 overflow-y-auto no-scrollbar">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600">
                <Key size={18} />
              </div>
              <div className="min-w-0">
                <span className="text-[7px] font-black text-indigo-300 uppercase block tracking-wider">Session Key</span>
                <code className="text-[9px] font-mono text-slate-500 break-all leading-tight opacity-70">
                  {user?.verificationHash.substr(0, 48)}...
                </code>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center text-amber-600">
                <Lock size={18} />
              </div>
              <div>
                <span className="text-[7px] font-black text-indigo-300 uppercase block tracking-wider">Storage</span>
                <span className="text-[10px] font-black text-slate-800 uppercase">Localized & Encrypted</span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600">
                <Zap size={18} />
              </div>
              <div>
                <span className="text-[7px] font-black text-indigo-300 uppercase block tracking-wider">Transmission</span>
                <span className="text-[10px] font-black text-slate-800 uppercase">P2P Secure Tunnel</span>
              </div>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <button 
          onClick={onLogout}
          className="w-full h-14 bg-white border-2 border-rose-100 text-rose-500 rounded-2xl flex items-center justify-center gap-3 font-black text-xs uppercase shadow-xl shadow-rose-100/30 shrink-0 transition-all active:scale-95 hover:bg-rose-50"
        >
          <LogOut size={18} />
          <span>Terminate Session</span>
        </button>
      </div>
    </div>
  );
};

export default ProfileScreen;
