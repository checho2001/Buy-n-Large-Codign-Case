const API_URL = 'http://127.0.0.1:8000/api';

export const getRole = async (username) => {
    try {
        const response = await fetch(`${API_URL}/role/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Credenciales inválidas');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
};