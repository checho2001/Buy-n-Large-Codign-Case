import React, { useState, useEffect } from 'react';

const Sidebar = ({ onSelectConversation }) => {
    const [recentConversations, setRecentConversations] = useState([]);
    const token = localStorage.getItem('jwt_token');

    useEffect(() => {
        fetchRecentConversations();
    }, []);

    const fetchRecentConversations = async () => {
        try {
            const headers = {
                'Content-Type': 'application/json',
            };

            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch('http://127.0.0.1:8000/api/chatbot/conversations/', {
                headers: headers,
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                setRecentConversations(data.conversations);
            }
        } catch (error) {
            console.error('Error fetching conversations:', error);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <aside style={{ 
            width: '250px', // Ancho fijo en lugar de porcentaje
            background: '#f0f0f5', 
            padding: '20px',
            borderRight: '1px solid #ddd',
            height: '100vh',
            overflowY: 'auto'
        }}>
            <div style={{ 
                textAlign: 'center',
                marginBottom: '20px',
                borderBottom: '1px solid #ddd',
                paddingBottom: '20px'
            }}>
                <img 
                    src="perfil.jpg" 
                    alt="Foto de perfil" 
                    style={{ 
                        borderRadius: '50%', 
                        width: '80px',
                        marginBottom: '10px'
                    }} 
                />
                <p style={{ margin: 0 }}>Perfil</p>
            </div>
            
            <nav>
                <div style={{ marginBottom: '20px' }}>
                    <p style={{ 
                        padding: '10px', 
                        margin: '5px 0',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        ':hover': { backgroundColor: '#e6e6e6' }
                    }}>Dashboard</p>
                    <p style={{ 
                        padding: '10px', 
                        margin: '5px 0',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        ':hover': { backgroundColor: '#e6e6e6' }
                    }}>Historial</p>
                </div>

                <h3 style={{ 
                    marginBottom: '15px',
                    fontSize: '1.1em',
                    color: '#333'
                }}>Conversaciones recientes</h3>

                <ul style={{ 
                    listStyle: 'none', 
                    padding: 0,
                    margin: 0
                }}>
                    {recentConversations.map((conv) => (
                        <li 
                            key={conv.id}
                            onClick={() => onSelectConversation(conv.id)}
                            style={{
                                padding: '10px',
                                marginBottom: '10px',
                                background: '#fff',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                transition: 'background-color 0.3s',
                                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                            }}
                            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#e6e6e6'}
                            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#fff'}
                        >
                            <div style={{ 
                                fontSize: '0.9em', 
                                fontWeight: 'bold',
                                marginBottom: '5px'
                            }}>
                                Conversación {conv.id.slice(0, 8)}...
                            </div>
                            <div style={{ 
                                fontSize: '0.8em', 
                                color: '#666',
                                marginBottom: '5px'
                            }}>
                                {formatDate(conv.created_at)}
                            </div>
                            <div style={{ 
                                fontSize: '0.8em', 
                                color: '#444',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap'
                            }}>
                                {conv.last_message?.slice(0, 30)}...
                            </div>
                        </li>
                    ))}
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;