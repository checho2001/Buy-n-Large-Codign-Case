const API_URL = 'http://localhost:8000/api';

export const login = async (email, password) => {
    const response = await fetch(`${API_URL}/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            password,
        }),
    });

    if (!response.ok) {
        throw new Error('Error en la autenticación');
    }

    return response.json();
};