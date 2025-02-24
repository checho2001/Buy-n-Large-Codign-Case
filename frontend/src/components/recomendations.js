import React from 'react';
import '../styles/Recommendations.css'; // Importa el archivo CSS

const Recommendations = ({ recommendations = [] }) => {
    console.log("Recomendaciones recibidas en componente:", recommendations);

    return (
        <aside className="recommendations-container">
            <h3 className="recommendations-header">Recomendados para ti</h3>
            
            {recommendations.length > 0 ? (
                <>
                    {/* Mejor Producto */}
                    {recommendations[0] && (
                        <div className="recommendation-item">
                            <h4 className="recommendation-title">✅ Mejor Producto</h4>
                            <p className="recommendation-brand">Marca: {recommendations[0].brand}</p>
                            <p className="recommendation-price">${recommendations[0].price.toFixed(2)}</p>
                            <p className="recommendation-stock">
                                {recommendations[0].stock > 0 
                                    ? `Stock disponible: ${recommendations[0].stock}` 
                                    : 'Sin stock'}
                            </p>
                            {recommendations[0].features && (
                                <div className="recommendation-features">
                                    <p>Características:</p>
                                    <ul>
                                        {Object.entries(recommendations[0].features).map(([key, value], i) => (
                                            <li key={i}>{`${key}: ${value}`}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Producto del Medio */}
                    {recommendations[1] && (
                        <div className="recommendation-item">
                            <h4 className="recommendation-title">🔹 Producto del Medio</h4>
                            <p className="recommendation-brand">Marca: {recommendations[1].brand}</p>
                            <p className="recommendation-price">${recommendations[1].price.toFixed(2)}</p>
                            <p className="recommendation-stock">
                                {recommendations[1].stock > 0 
                                    ? `Stock disponible: ${recommendations[1].stock}` 
                                    : 'Sin stock'}
                            </p>
                            {recommendations[1].features && (
                                <div className="recommendation-features">
                                    <p>Características:</p>
                                    <ul>
                                        {Object.entries(recommendations[1].features).map(([key, value], i) => (
                                            <li key={i}>{`${key}: ${value}`}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Peor Producto */}
                    {recommendations[2] && (
                        <div className="recommendation-item">
                            <h4 className="recommendation-title">❌ Peor Producto</h4>
                            <p className="recommendation-brand">Marca: {recommendations[2].brand}</p>
                            <p className="recommendation-price">${recommendations[2].price.toFixed(2)}</p>
                            <p className="recommendation-stock">
                                {recommendations[2].stock > 0 
                                    ? `Stock disponible: ${recommendations[2].stock}` 
                                    : 'Sin stock'}
                            </p>
                            {recommendations[2].features && (
                                <div className="recommendation-features">
                                    <p>Características:</p>
                                    <ul>
                                        {Object.entries(recommendations[2].features).map(([key, value], i) => (
                                            <li key={i}>{`${key}: ${value}`}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </>
            ) : (
                <div className="no-recommendations">No hay recomendaciones disponibles</div>
            )}
        </aside>
    );
};

export default Recommendations;