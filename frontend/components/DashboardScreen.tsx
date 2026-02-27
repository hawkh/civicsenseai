
import React from 'react';
import { CivicIssue } from '../types';
import { Activity, Target } from 'lucide-react';
import IssueListItem from './IssueListItem';

interface DashboardScreenProps {
  issues: CivicIssue[];
  onSelectIssue: (issue: CivicIssue) => void;
}

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
              onSelect={onSelectIssue}
            />
          ))
        )}
      </div>
    </div>
  );
};

// Fix: Add missing default export
export default DashboardScreen;
