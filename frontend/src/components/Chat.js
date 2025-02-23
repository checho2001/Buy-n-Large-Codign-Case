import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [sessionId, setSessionId] = useState(null);
    const [inputMessage, setInputMessage] = useState('');
    const { token } = useAuth();

    const startNewConversation = async () => {
        try {
            const response = await fetch('/api/chatbot/session/new', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            setSessionId(data.session_id);
            setMessages([]);
        } catch (error) {
            console.error('Error starting new conversation:', error);
        }
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim()) return;

        try {
            const response = await fetch('/api/chatbot/message', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: inputMessage,
                    session_id: sessionId
                })
            });
            const data = await response.json();
            setMessages(prev => [...prev, data]);
            setInputMessage('');
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div className="chat-container">
            <button onClick={startNewConversation}>
                Nueva Conversación
            </button>
            <div className="messages-container">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.is_bot ? 'bot' : 'user'}`}>
                        {msg.message_text}
                    </div>
                ))}
            </div>
            <form onSubmit={sendMessage}>
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Escribe tu mensaje..."
                />
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
};

export default Chat; 