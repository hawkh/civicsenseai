import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SupervisorDashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  const fetchTickets = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/tickets');
      setTickets(res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
    const interval = setInterval(fetchTickets, 5000); // Poll every 5s for updates
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return '#ffc107'; // yellow
      case 'in_progress': return '#17a2b8'; // blue
      case 'closed': return '#28a745'; // green
      case 'review_pending': return '#fd7e14'; // orange
      default: return '#6c757d';
    }
  };

  const filteredTickets = tickets.filter(t => filter === 'all' || t.status === filter);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Supervisor Dashboard</h1>

      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('open')}>Open</button>
        <button onClick={() => setFilter('in_progress')}>In Progress</button>
        <button onClick={() => setFilter('review_pending')}>Review Needed</button>
        <button onClick={() => setFilter('closed')}>Closed</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
        {filteredTickets.map(ticket => (
          <div key={ticket.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
              <strong>#{ticket.id}</strong>
              <span style={{
                background: getStatusColor(ticket.status),
                color: 'white',
                padding: '2px 8px',
                borderRadius: '10px',
                fontSize: '12px'
              }}>
                {ticket.status}
              </span>
            </div>

            {ticket.evidence && ticket.evidence.length > 0 && (
              <img
                src={`http://localhost:8000/uploads/${ticket.evidence[0].file_path.split('/').pop()}`} // Hacky path fix for demo
                alt="evidence"
                style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: '4px' }}
              />
            )}

            <div style={{ marginTop: '10px' }}>
              <p><strong>Type:</strong> {ticket.ticket?.issue_type || 'Analyzing...'}</p>
              <p><strong>Priority:</strong> {ticket.ticket?.priority || '-'}</p>
              <p><strong>Location:</strong> {ticket.location || 'Unknown'}</p>
              <p><strong>Source:</strong> {ticket.source}</p>
              <p style={{ fontSize: '14px', color: '#555' }}>{ticket.description}</p>
            </div>

            {ticket.ticket?.verification_score && (
               <div style={{ marginTop: '10px', padding: '5px', background: '#e9ecef' }}>
                 <strong>Verification Confidence:</strong> {(ticket.ticket.verification_score * 100).toFixed(1)}%
               </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SupervisorDashboard;
