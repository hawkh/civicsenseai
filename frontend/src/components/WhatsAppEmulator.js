import React, { useState } from 'react';
import axios from 'axios';

const WhatsAppEmulator = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [sender, setSender] = useState('+15551234567');

  const handleSendMessage = async () => {
    if (!inputText && !selectedFile) return;

    const newMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'me',
      file: selectedFile ? URL.createObjectURL(selectedFile) : null,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages([...messages, newMessage]);

    // Send to Backend
    const formData = new FormData();
    formData.append('text', inputText);
    formData.append('sender', sender);
    if (selectedFile) {
      formData.append('file', selectedFile);
    }

    try {
      const response = await axios.post('http://localhost:8000/api/v1/webhook/whatsapp', formData);

      // Auto-reply simulation
      const replyMessage = {
        id: Date.now() + 1,
        text: `Bot: Received! Ticket #${response.data.ticket_id} created.`,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, replyMessage]);

    } catch (error) {
      console.error("Error sending whatsapp message:", error);
    }

    setInputText('');
    setSelectedFile(null);
  };

  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '10px',
      width: '350px',
      height: '600px',
      display: 'flex',
      flexDirection: 'column',
      background: '#e5ddd5'
    }}>
      <div style={{ background: '#075e54', color: 'white', padding: '10px', borderTopLeftRadius: '10px', borderTopRightRadius: '10px' }}>
        <strong>WhatsApp Simulator</strong>
        <br/>
        <small>{sender}</small>
      </div>

      <div style={{ flex: 1, padding: '10px', overflowY: 'auto' }}>
        {messages.map(msg => (
          <div key={msg.id} style={{
            display: 'flex',
            justifyContent: msg.sender === 'me' ? 'flex-end' : 'flex-start',
            marginBottom: '10px'
          }}>
            <div style={{
              background: msg.sender === 'me' ? '#dcf8c6' : 'white',
              padding: '8px',
              borderRadius: '8px',
              maxWidth: '80%'
            }}>
              {msg.file && <img src={msg.file} alt="upload" style={{ maxWidth: '100%', borderRadius: '5px' }} />}
              <div>{msg.text}</div>
              <div style={{ fontSize: '10px', color: '#999', textAlign: 'right' }}>{msg.timestamp}</div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: '10px', background: '#f0f0f0', borderBottomLeftRadius: '10px', borderBottomRightRadius: '10px' }}>
        <input
          type="file"
          onChange={(e) => setSelectedFile(e.target.files[0])}
          style={{ marginBottom: '5px', fontSize: '12px' }}
        />
        <div style={{ display: 'flex' }}>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type a message"
            style={{ flex: 1, padding: '8px', borderRadius: '20px', border: 'none', marginRight: '5px' }}
          />
          <button onClick={handleSendMessage} style={{ background: '#075e54', color: 'white', border: 'none', borderRadius: '50%', width: '35px', height: '35px' }}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
};

export default WhatsAppEmulator;
