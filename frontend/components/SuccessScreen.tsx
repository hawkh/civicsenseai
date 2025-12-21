
import React from 'react';
import { Check, ArrowRight, PartyPopper } from 'lucide-react';

interface SuccessScreenProps {
  onDone: () => void;
}

const SuccessScreen: React.FC<SuccessScreenProps> = ({ onDone }) => {
  return (
    <div className="h-full w-full flex flex-col items-center justify-center p-8 text-center bg-white relative overflow-hidden">
      {/* Background celebration shapes */}
      <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-amber-400 rounded-full animate-ping opacity-40"></div>
      <div className="absolute bottom-1/4 right-1/4 w-3 h-3 bg-indigo-400 rounded-full animate-bounce opacity-40"></div>
      
      <div className="w-24 h-24 bg-emerald-50 text-emerald-500 rounded-[2.5rem] flex items-center justify-center mb-10 shadow-2xl shadow-emerald-100 animate-in zoom-in-50 duration-700">
        <Check size={48} strokeWidth={4} />
      </div>

      <div className="space-y-4 mb-16 relative z-10">
        <h2 className="text-5xl font-black tracking-tighter text-indigo-950 leading-tight">Broadcast<br/>Deployed.</h2>
        <p className="text-base text-slate-400 font-bold max-w-[240px] mx-auto leading-relaxed">
          AI has finalized your report and established a secure channel with the authorities.
        </p>
      </div>

      <button
        onClick={onDone}
        className="w-full max-w-sm bg-indigo-600 text-white font-black h-16 rounded-[2rem] flex items-center justify-center gap-4 shadow-2xl shadow-indigo-200 transition-all hover:bg-indigo-700 active:scale-95"
      >
        <span className="uppercase tracking-[0.2em] text-sm">Track Progress</span>
        <ArrowRight size={20} strokeWidth={3} />
      </button>
      
      <p className="mt-8 text-[10px] font-black text-emerald-600 uppercase tracking-widest">Incident #LIVE_ACTIVE</p>
    </div>
  );
};

export default SuccessScreen;
