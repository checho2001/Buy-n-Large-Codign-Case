import React from 'react';

const ProductCard = ({ productName, imageUrl }) => {
    return (
        <div style={{ border: '1px solid #ccc', padding: '10px', textAlign: 'center' }}>
            <img src={imageUrl} alt={productName} style={{ width: '100px' }} />
            <p>{productName}</p>
        </div>
    );
};

export default ProductCard;