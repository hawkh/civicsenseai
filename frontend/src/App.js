import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CitizenReport from './components/CitizenReport';
import SupervisorDashboard from './components/SupervisorDashboard';
import WhatsAppEmulator from './components/WhatsAppEmulator';
import TaskClosure from './components/TaskClosure';

function App() {
  return (
    <Router>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <nav style={{ padding: '20px', background: '#333', color: 'white', display: 'flex', gap: '20px' }}>
          <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Report (Web)</Link>
          <Link to="/whatsapp" style={{ color: 'white', textDecoration: 'none' }}>WhatsApp</Link>
          <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none' }}>Dashboard</Link>
          <Link to="/field" style={{ color: 'white', textDecoration: 'none' }}>Field Staff</Link>
        </nav>

        <div style={{ flex: 1, overflow: 'auto' }}>
          <Routes>
            <Route path="/" element={<CitizenReport />} />
            <Route path="/whatsapp" element={
              <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
                <WhatsAppEmulator />
              </div>
            } />
            <Route path="/dashboard" element={<SupervisorDashboard />} />
            <Route path="/field" element={<TaskClosure />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
