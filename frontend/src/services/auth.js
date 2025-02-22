const API_URL = 'http://127.0.0.1:8000/api';

export const login = async (username, password) => {
    try {
        const response = await fetch(`${API_URL}/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
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