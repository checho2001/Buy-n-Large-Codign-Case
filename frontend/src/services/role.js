const API_URL = 'http://127.0.0.1:8000/api';

export const getRole = async (token) => {
    try {
        const response = await fetch(`${API_URL}/users/role/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener el rol');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener el rol:', error);
        throw error;
    }
};