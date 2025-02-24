import React, { useState, useEffect } from 'react';
import { getCSRFToken } from '../utils/csrf';
import '../styles/Sidebar.css'; // Importa el archivo CSS

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
        <aside className="sidebar">
            <div className="sidebar-header">
                <img src="perfil.jpg" alt="Foto de perfil" />
                <p>Perfil</p>
            </div>
            
            <nav>
                <div>
                    <p className="nav-item">Dashboard</p>
                    <p className="nav-item">Historial</p>
                </div>

                <h3 className="recent-conversations">Conversaciones recientes</h3>

                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {recentConversations.map((conv) => (
                        <li 
                            key={conv.id}
                            onClick={() => onSelectConversation(conv.id)}
                            className="conversation-item"
                        >
                            <div className="conversation-title">
                                Conversación {conv.id.slice(0, 8)}...
                            </div>
                            <div className="conversation-date">
                                {formatDate(conv.created_at)}
                            </div>
                            <div className="conversation-last-message">
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