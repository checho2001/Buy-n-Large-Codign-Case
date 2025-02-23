import React from 'react';

const Recommendations = () => {
    return (
        <aside style={{ 
            width: '250px', 
            background: '#f0f0f5', 
            padding: '20px',
            borderLeft: '1px solid #ddd',
            height: '100vh',
            overflowY: 'auto'
        }}>
            <h3 style={{ marginBottom: '15px' }}>Recomendados para ti</h3>
            <div style={{ 
                background: '#fff',
                padding: '10px',
                borderRadius: '5px',
                marginBottom: '10px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
                <p>Producto Recomendado 1</p>
            </div>
            <div style={{ 
                background: '#fff',
                padding: '10px',
                borderRadius: '5px',
                marginBottom: '10px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
                <p>Producto Recomendado 2</p>
            </div>
            <div style={{ 
                background: '#fff',
                padding: '10px',
                borderRadius: '5px',
                marginBottom: '10px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
                <p>Producto Recomendado 3</p>
            </div>
        </aside>
    );
};

export default Recommendations;