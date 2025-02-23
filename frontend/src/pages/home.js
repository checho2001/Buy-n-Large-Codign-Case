import React, { useState } from 'react';
import Sidebar from '../components/sidebar';
import MainContent from '../components/MainContent';
import Recommendations from '../components/recomendations';

const Home = () => {
    const [selectedConversation, setSelectedConversation] = useState(null);

    const handleSelectConversation = (conversationId) => {
        setSelectedConversation(conversationId);
    };

    return (
        <div style={{ 
            display: 'flex', 
            minHeight: '100vh',
            maxHeight: '100vh',
            width: '100%',
            overflow: 'hidden',
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0
        }}>
            <Sidebar onSelectConversation={handleSelectConversation} />
            <MainContent selectedConversation={selectedConversation} />
            <Recommendations />
        </div>
    );
};

export default Home;