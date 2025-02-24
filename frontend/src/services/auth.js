const API_URL = 'http://127.0.0.1:8000/api';

export const login = async (username, password) => {
    try {
        const response = await fetch(`${API_URL}/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        if (!response.ok) {
            throw new Error('Error en la autenticación');
        }

        const data = await response.json();
        
        // Verificar que recibimos el token
        if (!data.access) {
            throw new Error('Token no recibido');
        }

        console.log('Login exitoso, token recibido'); // Para debugging
        return data;
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
};