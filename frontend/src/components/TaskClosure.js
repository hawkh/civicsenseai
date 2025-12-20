import React, { useState } from 'react';
import axios from 'axios';

const TaskClosure = () => {
  const [ticketId, setTicketId] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ticketId || !file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`http://localhost:8000/api/v1/tickets/${ticketId}/verify`, formData);
      setResult(res.data);
    } catch (err) {
      alert("Error verifying ticket. Check ID.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h2>Field Staff: Resolve Ticket</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Ticket ID:</label>
          <input
            type="number"
            value={ticketId}
            onChange={(e) => setTicketId(e.target.value)}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>Upload Proof of Work (Image):</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ width: '100%', marginTop: '5px' }}
          />
        </div>

        <button type="submit" disabled={loading} style={{
          width: '100%',
          padding: '10px',
          background: '#28a745',
          color: 'white',
          border: 'none',
          fontSize: '16px'
        }}>
          {loading ? 'Verifying...' : 'Submit & Verify'}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '20px', padding: '15px', background: result.verification_result.verified ? '#d4edda' : '#f8d7da' }}>
          <h3>Result: {result.status}</h3>
          <p>Matched: {result.verification_result.verified ? 'Yes' : 'No'}</p>
          <p>Confidence: {(result.verification_result.score * 100).toFixed(1)}%</p>
          <p>Reason: {result.verification_result.reason}</p>
        </div>
      )}
    </div>
  );
};

export default TaskClosure;
