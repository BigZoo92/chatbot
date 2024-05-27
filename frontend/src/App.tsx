import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App: React.FC = () => {
  const [message, setMessage] = useState<string>('');
  const [chatHistory, setChatHistory] = useState<{ sender: string, text: string }[]>([]);

  const sendMessage = async () => {
    if (message.trim() === '') return;

    const userMessage = { sender: 'user', text: message };
    setChatHistory([...chatHistory, userMessage]);

    try {
      const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/chat`, { message });
      const botMessage = { sender: 'bot', text: res.data.response };
      setChatHistory([...chatHistory, userMessage, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setMessage('');
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <div className="chat-window">
        {chatHistory.map((chat, index) => (
          <div key={index} className={`chat-message ${chat.sender}`}>
            <p>{chat.text}</p>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;
