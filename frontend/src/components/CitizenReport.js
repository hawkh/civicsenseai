import React, { useState } from 'react';
import axios from 'axios';

function CitizenReport() {
  const [description, setDescription] = useState('');
  const [contactInfo, setContactInfo] = useState('');
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please upload an image.');
      return;
    }

    const formData = new FormData();
    formData.append('description', description);
    formData.append('contact_info', contactInfo);
    formData.append('source', 'web');
    formData.append('file', file);

    try {
      const response = await axios.post('/api/v1/reports', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(`Report submitted! ID: ${response.data.id}`);
      setDescription('');
      setFile(null);
    } catch (error) {
      setMessage('Error submitting report.');
      console.error(error);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Report an Issue</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Description:</label>
          <br />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="4"
            style={{ width: '100%' }}
            required
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Contact Info (Optional):</label>
          <br />
          <input
            type="text"
            value={contactInfo}
            onChange={(e) => setContactInfo(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Upload Evidence:</label>
          <br />
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            accept="image/*"
            required
          />
        </div>
        <button type="submit">Submit Report</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default CitizenReport;
