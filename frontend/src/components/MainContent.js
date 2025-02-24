import React, { useState, useEffect, useRef } from 'react';
import { getCSRFToken } from '../utils/csrf';
import '../styles/MainContent.css';

const MainContent = ({ selectedConversation, onRecommendationsUpdate }) => {
    const [inputText, setInputText] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const [sessionId, setSessionId] = useState(null);
    const [sessionInfo, setSessionInfo] = useState(null);
    const token = localStorage.getItem('jwt_token');

    // Efecto para cargar mensajes cuando se selecciona una conversación
    useEffect(() => {
        if (selectedConversation) {
            setSessionId(selectedConversation);
            loadConversationMessages(selectedConversation);
        }
    }, [selectedConversation]);

    const loadConversationMessages = async (conversationId) => {
        try {
            const headers = {
                'Content-Type': 'application/json',
            };
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`http://127.0.0.1:8000/api/chatbot/conversations/${conversationId}/messages/`, {
                headers: headers,
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                setMessages(data.messages.map(msg => ({
                    text: msg.message_text,
                    isBot: msg.is_bot
                })));
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    };

    const sendMessage = async () => {
        if (!inputText.trim()) return;
        setIsLoading(true);

        try {
            const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            };

            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch('http://127.0.0.1:8000/api/chatbot/', {
                method: 'POST',
                headers: headers,
                credentials: 'include',
                body: JSON.stringify({
                    message: inputText,
                    session_id: sessionId
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.session_id) {
                setSessionId(data.session_id);
            }

            setMessages(prevMessages => [
                ...prevMessages,
                { text: data.messages.user_message.text, isBot: false },
                { text: data.messages.bot_message.text, isBot: true }
            ]);

            if (onRecommendationsUpdate && data.recommendations) {
                onRecommendationsUpdate(data.recommendations);
            }

        } catch (error) {
            console.error('Error:', error);
            setMessages(prevMessages => [
                ...prevMessages,
                { text: inputText, isBot: false },
                { text: 'Error al procesar tu mensaje. Por favor, intenta de nuevo.', isBot: true }
            ]);
        } finally {
            setIsLoading(false);
            setInputText('');
        }
    };

    // Scroll automático
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <main className="main-content">
            <div className="header">
                <span>🤖</span>
                <strong>Hola, ¿En qué puedo ayudarte?</strong>
            </div>

            <div className="messages-container">
                {messages.map((message, index) => (
                    <div key={index} style={{ display: 'flex', justifyContent: message.isBot ? 'flex-start' : 'flex-end', marginBottom: '15px' }}>
                        <div style={{ background: message.isBot ? '#f0f0f5' : '#007bff', color: message.isBot ? '#000' : '#fff', padding: '12px 16px', borderRadius: '15px', maxWidth: '70%', wordWrap: 'break-word', boxShadow: '0 1px 2px rgba(0,0,0,0.1)' }}>
                            {message.text}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {isLoading && (
                <div className="loading">
                    <span>Cargando...</span>
                </div>
            )}

            <div className="input-container">
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Escribe tu pregunta aquí..."
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') sendMessage();
                    }}
                />
                <button onClick={sendMessage}>Enviar</button>
            </div>
        </main>
    );
};

export default MainContent;