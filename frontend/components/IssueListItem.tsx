import React from 'react';
import { CivicIssue, IssueStatus } from '../types';
import { ChevronRight } from 'lucide-react';

interface IssueListItemProps {
  issue: CivicIssue;
  onClick: (issue: CivicIssue) => void;
}

const IssueListItem: React.FC<IssueListItemProps> = React.memo(({ issue, onClick }) => {
  return (
    <button
      onClick={() => onClick(issue)}
      className="w-full bg-white p-3 rounded-2xl shadow-lg shadow-indigo-100/20 border border-white flex items-center gap-4 transition-all active:scale-[0.98] group shrink-0"
    >
      <div className="w-12 h-12 rounded-xl overflow-hidden shrink-0 shadow-sm">
        <img src={issue.image} alt="" className="w-full h-full object-cover" />
      </div>

      <div className="flex-1 text-left min-w-0">
        <div className="flex items-center gap-1.5 mb-0.5">
          <span className={`w-2 h-2 rounded-full ${
            issue.status === IssueStatus.VERIFIED ? 'bg-emerald-400' :
            (issue.status === IssueStatus.ROUTED || issue.status === IssueStatus.CLASSIFIED) ? 'bg-amber-400 animate-pulse' : 'bg-indigo-300'
          }`}></span>
          <span className="text-[8px] font-black text-indigo-400 uppercase truncate">{issue.category}</span>
        </div>
        <h4 className="text-base font-black text-indigo-950 truncate">#{issue.id.substring(issue.id.length - 6).toUpperCase()}</h4>
      </div>

      <ChevronRight size={16} className="text-indigo-200 group-hover:text-indigo-600 transition-colors" />
    </button>
  );
});

export default IssueListItem;
