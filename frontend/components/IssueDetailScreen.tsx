
import React, { useState } from 'react';
import { CivicIssue, IssueStatus } from '../types.ts';
import { ArrowLeft, MapPin, Calendar, Building2, Trash2, AlertCircle } from 'lucide-react';

interface IssueDetailScreenProps {
  issue: CivicIssue;
  onBack: () => void;
  onDelete: () => void;
}

const IssueDetailScreen: React.FC<IssueDetailScreenProps> = ({ issue, onBack, onDelete }) => {
  const [showConfirm, setShowConfirm] = useState(false);

const statusSteps = [
  { label: 'Submitted', key: IssueStatus.SUBMITTED },
  { label: 'Classified', key: IssueStatus.CLASSIFIED },
  { label: 'Routed', key: IssueStatus.ROUTED },
  { label: 'Verified', key: IssueStatus.VERIFIED },
];


  const currentStepIndex = statusSteps.findIndex(s => s.key === issue.status);

  return (
    <div className="h-full flex flex-col bg-white overflow-hidden">
      <header className="px-4 py-3 flex justify-between items-center border-b border-indigo-50 shrink-0">
        <button onClick={onBack} className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
          <ArrowLeft size={18} strokeWidth={3} />
        </button>
        <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Detail View</span>
        <button onClick={() => setShowConfirm(true)} className="p-2 bg-rose-50 text-rose-500 rounded-xl">
          <Trash2 size={18} />
        </button>
      </header>

      <div className="flex-1 flex flex-col p-4 gap-4 min-h-0 overflow-hidden">
        <div className="shrink-0 w-full max-h-[25vh] rounded-3xl overflow-hidden shadow-lg border-2 border-white">
          <img src={issue.image} alt={issue.category} className="w-full h-full object-cover" />
        </div>

        <div className="shrink-0 flex items-center justify-between">
          <h2 className="text-2xl font-black text-indigo-950 leading-none truncate pr-4">{issue.category}</h2>
          <span className={`shrink-0 px-3 py-1 rounded-full text-[8px] font-black uppercase ${
            issue.severity === 'High' ? 'bg-amber-500 text-white' : 'bg-emerald-500 text-white'
          }`}>
            {issue.severity}
          </span>
        </div>
        
        <div className="shrink-0 bg-indigo-50/50 p-4 rounded-2xl border border-indigo-100">
          <p className="text-slate-700 font-bold text-xs leading-snug line-clamp-3">{issue.description}</p>
        </div>

        <div className="flex-1 bg-white border border-indigo-50 rounded-2xl p-4 shadow-sm overflow-hidden flex flex-col gap-4">
          <div className="grid grid-cols-2 gap-3 shrink-0">
             <div className="space-y-0.5">
               <span className="text-[8px] font-black text-indigo-300 uppercase">Unit</span>
               <div className="flex items-center gap-1.5 truncate">
                 <Building2 size={12} className="text-indigo-400 shrink-0" />
                 <span className="text-[10px] font-black truncate">{issue.department}</span>
               </div>
             </div>
             <div className="space-y-0.5">
               <span className="text-[8px] font-black text-indigo-300 uppercase">GPS</span>
               <div className="flex items-center gap-1.5 truncate">
                 <MapPin size={12} className="text-indigo-400 shrink-0" />
                 <span className="text-[10px] font-black truncate font-mono">{issue.location.latitude.toFixed(4)}...</span>
               </div>
             </div>
          </div>

          <div className="flex-1 border-t border-indigo-50 pt-3 overflow-hidden flex flex-col gap-3">
             <span className="text-[8px] font-black text-indigo-300 uppercase">Tracking Flow</span>
             <div className="flex justify-between items-center relative px-2">
                <div className="absolute left-2 right-2 top-2 h-0.5 bg-indigo-50 rounded-full" />
                {statusSteps.map((step, idx) => {
                  const isActive = idx <= currentStepIndex;
                  return (
                    <div key={step.key} className="relative z-10 flex flex-col items-center gap-1">
                      <div className={`w-4 h-4 rounded-full border-2 border-white shadow-sm ${isActive ? 'bg-indigo-600' : 'bg-indigo-50'}`} />
                      <span className={`text-[7px] font-black uppercase ${isActive ? 'text-indigo-600' : 'text-slate-300'}`}>{step.label}</span>
                    </div>
                  );
                })}
             </div>
          </div>
        </div>
      </div>

      {showConfirm && (
        <div className="absolute inset-0 z-[100] bg-indigo-950/80 backdrop-blur-sm flex items-center justify-center p-6">
          <div className="bg-white rounded-[2rem] p-6 w-full max-w-xs text-center shadow-2xl animate-in zoom-in-95 duration-200">
            <AlertCircle size={32} className="text-rose-500 mx-auto mb-4" />
            <h4 className="text-lg font-black text-slate-800 mb-2">Terminate Report?</h4>
            <div className="flex flex-col gap-2">
              <button onClick={onDelete} className="w-full py-4 bg-rose-500 text-white font-black rounded-xl text-xs uppercase tracking-widest">Delete</button>
              <button onClick={() => setShowConfirm(false)} className="w-full py-3 text-slate-400 font-black text-xs uppercase">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Fix: Add missing default export
export default IssueDetailScreen;
