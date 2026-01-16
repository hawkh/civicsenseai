
import React, { useState, useEffect, useCallback } from 'react';
import { AppState, CivicIssue, User, IssueStatus } from './types';
import AuthScreen from './components/AuthScreen';
import HomeScreen from './components/HomeScreen';
import ReportScreen from './components/ReportScreen';
import DashboardScreen from './components/DashboardScreen';
import SuccessScreen from './components/SuccessScreen';
import ProfileScreen from './components/ProfileScreen';
import IssueDetailScreen from './components/IssueDetailScreen';
import { Plus, LayoutGrid, User as UserIcon, Shield, Sparkles } from 'lucide-react';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<AppState>(AppState.AUTH);
  const [user, setUser] = useState<User | null>(null);
  const [issues, setIssues] = useState<CivicIssue[]>([]);
  const [selectedIssue, setSelectedIssue] = useState<CivicIssue | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('civic_issues');
    if (saved) {
      setIssues(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('civic_issues', JSON.stringify(issues));
  }, [issues]);

useEffect(() => {
  if (issues.length === 0) return;

  const interval = setInterval(() => {
    setIssues(prevIssues => {
      const indexToUpdate = Math.floor(Math.random() * prevIssues.length);
      const issue = prevIssues[indexToUpdate];
      if (!issue || issue.status === IssueStatus.VERIFIED) return prevIssues;

      let nextStatus = issue.status;

      if (issue.status === IssueStatus.SUBMITTED) {
        nextStatus = IssueStatus.CLASSIFIED;
      } else if (issue.status === IssueStatus.CLASSIFIED) {
        nextStatus = IssueStatus.ROUTED;
      } else if (issue.status === IssueStatus.ROUTED) {
        if (Math.random() > 0.8) {
          nextStatus = IssueStatus.VERIFIED;
        }
      }

      if (nextStatus === issue.status) return prevIssues;

      const updated = [...prevIssues];
      updated[indexToUpdate] = { ...issue, status: nextStatus };
      return updated;
    });
  }, 15000);

  return () => clearInterval(interval);
}, [issues.length]);


  const handleLogin = useCallback((newUser: User) => {
    setUser(newUser);
    setCurrentPage(AppState.HOME);
  }, []);

  const handleIssueSubmit = useCallback((newIssue: CivicIssue) => {
    setIssues(prev => [newIssue, ...prev]);
    setSelectedIssue(newIssue);
    setCurrentPage(AppState.SUCCESS);
  }, []);

  const handleDeleteIssue = useCallback((id: string) => {
    setIssues(prev => prev.filter(i => i.id !== id));
    setCurrentPage(AppState.DASHBOARD);
  }, []);

  const navigate = useCallback((page: AppState) => {
    setCurrentPage(page);
  }, []);

  const openIssueDetail = useCallback((issue: CivicIssue) => {
    setSelectedIssue(issue);
    setCurrentPage(AppState.ISSUE_DETAIL);
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case AppState.AUTH: return <AuthScreen onLogin={handleLogin} />;
      case AppState.HOME: return <HomeScreen user={user} onStartReport={() => navigate(AppState.REPORT)} />;
      case AppState.REPORT: return <ReportScreen onCancel={() => navigate(AppState.HOME)} onSubmit={handleIssueSubmit} />;
      case AppState.DASHBOARD: return <DashboardScreen issues={issues} onSelectIssue={openIssueDetail} />;
      case AppState.SUCCESS: return <SuccessScreen onDone={() => navigate(AppState.DASHBOARD)} />;
      case AppState.PROFILE: return <ProfileScreen user={user} onLogout={() => navigate(AppState.AUTH)} />;
      case AppState.ISSUE_DETAIL:
        return selectedIssue ? (
          <IssueDetailScreen 
            issue={selectedIssue} 
            onBack={() => navigate(AppState.DASHBOARD)} 
            onDelete={() => handleDeleteIssue(selectedIssue.id)}
          />
        ) : <DashboardScreen issues={issues} onSelectIssue={openIssueDetail} />;
      default: return <HomeScreen user={user} onStartReport={() => navigate(AppState.REPORT)} />;
    }
  };

  const isFullScreenPage = [AppState.AUTH, AppState.REPORT, AppState.SUCCESS, AppState.ISSUE_DETAIL].includes(currentPage);
  const showNav = !isFullScreenPage;

  const NavItem = ({ page, icon: Icon, label }: { page: AppState, icon: any, label: string }) => {
    const active = currentPage === page;
    return (
      <button 
        onClick={() => navigate(page)}
        className={`flex items-center gap-3 px-5 py-3 rounded-2xl transition-all duration-300 w-full ${
          active 
            ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-200' 
            : 'text-slate-400 hover:text-indigo-600 hover:bg-indigo-50'
        }`}
      >
        <Icon size={20} />
        <span className="text-sm font-bold tracking-tight">{label}</span>
      </button>
    );
  };

  return (
    <div className="fixed inset-0 flex flex-col md:flex-row bg-[#F8FAFF] overflow-hidden font-sans">
      {/* Sidebar - Desktop */}
      {showNav && (
        <aside className="hidden md:flex w-72 border-r border-indigo-50 bg-white flex-col p-8 shrink-0">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-200">
              <Shield size={22} fill="currentColor" />
            </div>
            <div className="flex flex-col">
              <span className="font-black text-slate-900 leading-tight">CIVIC SENSE AI</span>
              <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest">Digital City</span>
            </div>
          </div>
          
          <nav className="flex-1 space-y-3">
            <NavItem page={AppState.HOME} icon={Sparkles} label="New Report" />
            <NavItem page={AppState.DASHBOARD} icon={LayoutGrid} label="My Dashboard" />
            <NavItem page={AppState.PROFILE} icon={UserIcon} label="Digital ID" />
          </nav>
        </aside>
      )}

      {/* Main Content */}
      <main className="flex-1 relative flex flex-col overflow-hidden">
        <div className={`flex-1 overflow-hidden flex flex-col ${isFullScreenPage ? '' : 'max-w-5xl mx-auto w-full'}`}>
          {renderPage()}
        </div>

        {/* Bottom Nav - Mobile */}
        {showNav && (
          <nav className="md:hidden glass border-t border-indigo-50 flex justify-around items-center h-20 shrink-0 px-6 z-50 rounded-t-[2.5rem] shadow-[0_-10px_40px_rgba(79,70,229,0.05)] pb-safe">
            <button onClick={() => navigate(AppState.HOME)} className={`p-4 transition-all duration-300 rounded-2xl ${currentPage === AppState.HOME ? 'text-indigo-600 bg-indigo-50' : 'text-slate-400'}`}>
              <Plus size={24} />
            </button>
            <button onClick={() => navigate(AppState.DASHBOARD)} className={`p-4 transition-all duration-300 rounded-2xl ${currentPage === AppState.DASHBOARD ? 'text-indigo-600 bg-indigo-50' : 'text-slate-400'}`}>
              <LayoutGrid size={24} />
            </button>
            <button onClick={() => navigate(AppState.PROFILE)} className={`p-4 transition-all duration-300 rounded-2xl ${currentPage === AppState.PROFILE ? 'text-indigo-600 bg-indigo-50' : 'text-slate-400'}`}>
              <UserIcon size={24} />
            </button>
          </nav>
        )}
      </main>
    </div>
  );
};

export default App;
