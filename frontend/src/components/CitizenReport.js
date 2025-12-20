import React, { useState, useRef } from 'react';
import axios from 'axios';

function CitizenReport() {
  const [description, setDescription] = useState('');
  const [contactInfo, setContactInfo] = useState('');
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);

  // Use useRef to store chunks to avoid closure issues in onstop callback
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = []; // Reset chunks

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        // Create a File object from the Blob
        const audioFile = new File([audioBlob], "voice_report.webm", { type: "audio/webm" });
        setFile(audioFile);
        audioChunksRef.current = []; // Clear chunks
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setMessage("Error accessing microphone.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      // Stop all tracks to release microphone
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file && !description) {
      setMessage('Please upload an image/audio or provide a description.');
      return;
    }

    const formData = new FormData();
    formData.append('description', description);
    formData.append('contact_info', contactInfo);
    formData.append('source', 'web');
    if (file) {
      formData.append('file', file);
    }

    try {
      setMessage('Submitting...');
      const response = await axios.post('/api/v1/reports', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      let msg = `Report submitted! ID: ${response.data.id}`;
      if (response.data.description && response.data.description !== description) {
         msg += ` (Transcribed: ${response.data.description})`;
      }
      setMessage(msg);

      setDescription('');
      setContactInfo('');
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
            placeholder="Describe the issue or record voice..."
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
            <label>Voice Input:</label><br/>
            {!isRecording ? (
                <button type="button" onClick={startRecording} style={{backgroundColor: '#4CAF50', color: 'white', padding: '10px', border: 'none', borderRadius: '5px', cursor: 'pointer'}}>
                    🎤 Start Recording
                </button>
            ) : (
                <button type="button" onClick={stopRecording} style={{backgroundColor: '#f44336', color: 'white', padding: '10px', border: 'none', borderRadius: '5px', cursor: 'pointer'}}>
                    ⏹ Stop Recording
                </button>
            )}
            {file && file.type.startsWith('audio') && <span style={{marginLeft: '10px'}}>Audio recorded ready to submit.</span>}
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
          <label>Upload Evidence (Image/Audio):</label>
          <br />
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            accept="image/*,audio/*,video/*"
          />
        </div>
        <button type="submit" style={{padding: '10px 20px', fontSize: '16px'}}>Submit Report</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default CitizenReport;
