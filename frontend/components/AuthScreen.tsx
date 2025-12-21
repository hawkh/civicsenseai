
import React, { useState } from 'react';
import { User } from '../types';
import { Shield, ArrowRight, Zap } from 'lucide-react';

interface AuthScreenProps {
  onLogin: (user: User) => void;
}

const AuthScreen: React.FC<AuthScreenProps> = ({ onLogin }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = () => {
    setIsLoading(true);
    setTimeout(() => {
      onLogin({
        id: 'u_' + Math.random().toString(36).substring(7),
        isVerified: true,
        verificationHash: 'sha256_' + Math.random().toString(36).substring(5)
      });
    }, 1500);
  };

  return (
    <div className="h-full w-full flex flex-col items-center justify-center p-6 md:p-8 text-center bg-white relative overflow-hidden">
      {/* Background blobs */}
      <div className="absolute top-[-10%] right-[-10%] w-64 md:w-96 h-64 md:h-96 bg-indigo-100 rounded-full blur-[80px] md:blur-[120px] opacity-60"></div>
      <div className="absolute bottom-[-10%] left-[-10%] w-64 md:w-96 h-64 md:h-96 bg-amber-100 rounded-full blur-[80px] md:blur-[120px] opacity-60"></div>
      
      <div className="relative z-10 w-full max-w-sm space-y-8 md:space-y-12">
        <div className="mx-auto w-14 h-14 md:w-16 md:h-16 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-2xl md:rounded-[2rem] flex items-center justify-center text-white shadow-2xl shadow-indigo-200 float">
          <Shield size={28} md:size={32} fill="rgba(255,255,255,0.2)" />
        </div>

        <div className="space-y-3 md:space-y-4">
          <div className="flex items-center justify-center gap-2 mb-1 md:mb-2">
            <Zap size={14} className="text-amber-500 fill-amber-500" />
            <span className="text-[8px] md:text-[10px] font-black uppercase tracking-[0.3em] text-indigo-500">Next Gen Gov</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tighter text-slate-900 leading-[0.9]">
            CIVIC SENSE<br/>AI
          </h1>
          <p className="text-xs md:text-sm font-bold text-slate-400 max-w-[220px] md:max-w-[240px] mx-auto">
            High-trust, anonymous reporting platform for the modern citizen.
          </p>
        </div>

        <div className="space-y-4 md:space-y-6">
          <button
            onClick={handleLogin}
            disabled={isLoading}
            className="w-full bg-indigo-600 text-white font-black py-4 md:py-5 rounded-2xl md:rounded-[2rem] flex items-center justify-center gap-3 transition-all hover:bg-indigo-700 hover:shadow-2xl hover:shadow-indigo-200 active:scale-95 disabled:opacity-50 shadow-xl shadow-indigo-100"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-[3px] border-white/20 border-t-white rounded-full animate-spin"></div>
            ) : (
              <>
                <span className="uppercase tracking-widest text-[12px] md:text-sm">Secure Entry</span>
                <ArrowRight size={18} md:size={20} />
              </>
            )}
          </button>
          
          <div className="flex items-center justify-center gap-4">
             <div className="h-px bg-slate-100 flex-1"></div>
             <p className="text-[9px] text-slate-300 font-black uppercase tracking-widest">Encrypted</p>
             <div className="h-px bg-slate-100 flex-1"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthScreen;
