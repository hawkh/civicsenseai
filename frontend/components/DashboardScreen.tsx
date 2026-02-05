
import React, { memo } from 'react';
import { CivicIssue, IssueStatus } from '../types';
import { ChevronRight, Activity, Target } from 'lucide-react';

interface DashboardScreenProps {
  issues: CivicIssue[];
  onSelectIssue: (issue: CivicIssue) => void;
}

const IssueListItem = memo(({ issue, onClick }: { issue: CivicIssue; onClick: (issue: CivicIssue) => void }) => {
  return (
    <button
      onClick={() => onClick(issue)}
      className="w-full bg-white p-3 rounded-2xl shadow-lg shadow-indigo-100/20 border border-white flex items-center gap-4 transition-all active:scale-[0.98] group shrink-0"
    >
      <div className="w-12 h-12 rounded-xl overflow-hidden shrink-0 shadow-sm">
        <img src={issue.image_url} alt="" className="w-full h-full object-cover" />
      </div>

      <div className="flex-1 text-left min-w-0">
        <div className="flex items-center gap-1.5 mb-0.5">
          <span className={`w-2 h-2 rounded-full ${
            issue.status === IssueStatus.RESOLVED ? 'bg-emerald-400' :
            issue.status === IssueStatus.IN_PROGRESS ? 'bg-amber-400 animate-pulse' : 'bg-indigo-300'
          }`}></span>
          <span className="text-[8px] font-black text-indigo-400 uppercase truncate">{issue.category || 'Uncategorized'}</span>
        </div>
        <h4 className="text-base font-black text-indigo-950 truncate">#{issue.id.substr(-6).toUpperCase()}</h4>
      </div>

      <ChevronRight size={16} className="text-indigo-200 group-hover:text-indigo-600 transition-colors" />
    </button>
  );
});

const DashboardScreen: React.FC<DashboardScreenProps> = ({ issues, onSelectIssue }) => {
  return (
    <div className="h-full flex flex-col bg-[#F8FAFF] overflow-hidden">
      <header className="p-6 pb-2 shrink-0 flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-black tracking-tighter text-indigo-950 uppercase leading-none">Hub</h2>
          <p className="text-[9px] font-black text-indigo-400 uppercase tracking-[0.2em]">Active Stream</p>
        </div>
        <div className="w-8 h-8 bg-white rounded-lg shadow-sm border border-indigo-50 flex items-center justify-center text-indigo-500">
           <Activity size={16} />
        </div>
      </header>

      <div className="flex-1 overflow-y-auto no-scrollbar p-4 flex flex-col gap-3 min-h-0">
        {issues.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center gap-4 opacity-60">
            <Target size={32} className="text-indigo-200" />
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Zero Incidents</p>
          </div>
        ) : (
          issues.map((issue) => (
            <IssueListItem
              key={issue.id}
              issue={issue}
              onClick={onSelectIssue}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default DashboardScreen;
