import React, { useState } from 'react';
import Sidebar from '../components/sidebar';
import MainContent from '../components/MainContent';
import Recommendations from '../components/recomendations';
import '../styles/Home.css';

const Home = () => {
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [recommendations, setRecommendations] = useState([]);

    const handleSelectConversation = (conversationId) => {
        setSelectedConversation(conversationId);
    };

    const handleRecommendationsUpdate = (newRecommendations) => {
        console.log("Nuevas recomendaciones recibidas:", newRecommendations);
        setRecommendations(newRecommendations);
    };

    return (
        <div className="home-container">
            <Sidebar onSelectConversation={handleSelectConversation} />
            <MainContent 
                selectedConversation={selectedConversation} 
                onRecommendationsUpdate={handleRecommendationsUpdate}
            />
            <Recommendations recommendations={recommendations} />
        </div>
    );
};

export default Home;