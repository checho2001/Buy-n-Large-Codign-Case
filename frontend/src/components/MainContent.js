import React, { useState, useEffect, useRef } from 'react';

const MainContent = ({ selectedConversation }) => {
    const [inputText, setInputText] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const [sessionId, setSessionId] = useState(null);
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

            const response = await fetch(`http://127.0.0.1:8000/api/chatbot/messages/${conversationId}`, {
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
                'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
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
                { text: inputText, isBot: false },
                { text: data.messages.bot_message.text, isBot: true }
            ]);

        } catch (error) {
            console.error('Error:', error);
            setMessages(prevMessages => [
                ...prevMessages,
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
        <main style={{ 
            flex: 1, 
            padding: '20px', 
            display: 'flex', 
            flexDirection: 'column', 
            height: '100vh',
            backgroundColor: '#ffffff'
        }}>
            <div style={{ 
                background: '#e0e0ff', 
                padding: '15px', 
                borderRadius: '10px', 
                marginBottom: '20px',
                marginTop: '20px',  // Añadido margen superior
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
            }}>
                <span style={{ fontSize: '24px' }}>🤖</span>
                <strong style={{ fontSize: '16px' }}>Hola, ¿en qué puedo ayudarte?</strong>
            </div>

            <div style={{ 
                flex: 1, 
                overflowY: 'auto', 
                marginBottom: '20px', 
                border: '1px solid #ccc', 
                borderRadius: '10px', 
                padding: '20px',
                backgroundColor: '#f8f9fa'
            }}>
                {messages.map((message, index) => (
                    <div
                        key={index}
                        style={{
                            display: 'flex',
                            justifyContent: message.isBot ? 'flex-start' : 'flex-end',
                            marginBottom: '15px',
                        }}
                    >
                        <div
                            style={{
                                background: message.isBot ? '#f0f0f5' : '#007bff',
                                color: message.isBot ? '#000' : '#fff',
                                padding: '12px 16px',
                                borderRadius: '15px',
                                maxWidth: '70%',
                                wordWrap: 'break-word',
                                boxShadow: '0 1px 2px rgba(0,0,0,0.1)'
                            }}
                        >
                            {message.text}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {isLoading && (
                <div style={{ 
                    textAlign: 'center', 
                    marginBottom: '15px',
                    color: '#666'
                }}>
                    <span>Cargando...</span>
                </div>
            )}

            <div style={{ 
                display: 'flex', 
                gap: '10px',
                padding: '10px',
                backgroundColor: '#ffffff',
                borderTop: '1px solid #eee'
            }}>
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Escribe tu pregunta aquí..."
                    style={{ 
                        flex: 1, 
                        padding: '12px', 
                        borderRadius: '8px', 
                        border: '1px solid #ccc',
                        fontSize: '14px'
                    }}
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') sendMessage();
                    }}
                />
                <button
                    onClick={sendMessage}
                    style={{ 
                        background: '#007bff', 
                        color: 'white', 
                        padding: '12px 24px', 
                        borderRadius: '8px', 
                        border: 'none', 
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        transition: 'background-color 0.2s'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#0056b3'}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#007bff'}
                >
                    Enviar
                </button>
            </div>
        </main>
    );
};

export default MainContent;