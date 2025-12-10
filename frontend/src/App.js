import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CitizenReport from './components/CitizenReport';
import SupervisorDashboard from './components/SupervisorDashboard';

function App() {
  return (
    <Router>
      <div>
        <nav style={{ padding: '20px', background: '#f0f0f0', marginBottom: '20px' }}>
          <Link to="/" style={{ marginRight: '20px' }}>Citizen Report</Link>
          <Link to="/dashboard">Supervisor Dashboard</Link>
        </nav>

        <Routes>
          <Route path="/" element={<CitizenReport />} />
          <Route path="/dashboard" element={<SupervisorDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
