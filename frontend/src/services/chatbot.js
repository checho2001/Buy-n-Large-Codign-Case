const API_URL = 'http://127.0.0.1:8000/api/chatbot';

// Crear una nueva sesión de chat
export const createSession = async (userId) => {
    try {
        const response = await fetch(`${API_URL}/sessions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ user: userId }),
        });

        if (!response.ok) {
            throw new Error('Error al crear la sesión');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en createSession:', error);
        throw error;
    }
};

// Enviar un mensaje en una sesión de chat
export const sendMessage = async (sessionId, messageText, isBot = false, productId = null) => {
    try {
        const response = await fetch(`${API_URL}/sessions/${sessionId}/send_message/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                message_text: messageText,
                is_bot: isBot,
                product: productId,
            }),
        });

        if (!response.ok) {
            throw new Error('Error al enviar el mensaje');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en sendMessage:', error);
        throw error;
    }
};

// Obtener los mensajes de una sesión de chat
export const getMessages = async (sessionId) => {
    try {
        const response = await fetch(`${API_URL}/sessions/${sessionId}/get_messages/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener los mensajes');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en getMessages:', error);
        throw error;
    }
};

// Finalizar una sesión de chat
export const endSession = async (sessionId) => {
    try {
        const response = await fetch(`${API_URL}/sessions/${sessionId}/end_session/`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error al finalizar la sesión');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en endSession:', error);
        throw error;
    }
};