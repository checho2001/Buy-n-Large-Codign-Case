import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/auth';  // Importar el servicio de autenticación
import { getRole } from '../services/role';  // Importar el servicio de roles

const Login = () => {
    const [username, setUsername] = useState('');  // Cambiar email por username
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const data = await login(username, password);
            localStorage.setItem('token', data.access);
            
            // Obtener el rol del usuario
            const roleData = await getRole(data.access);
            
            // Redirigir según el rol
            if (roleData.role === 'admin') {
                navigate('/dashboard');
            } else {
                navigate('/home');
            }
        } catch (err) {
            setError('Usuario o contraseña incorrectos');
        }
    };

    return (
        <div style={styles.body}>
            <div style={styles.container}>
                <h2 style={styles.h2}>Bienvenido(a)</h2>
                <form onSubmit={handleLogin}>
                    <label>Usuario</label>  
                    <input
                        type="text"  
                        placeholder="Ingresa tu usuario"
                        value={username}  
                        onChange={(e) => setUsername(e.target.value)}  
                        required
                        style={styles.input}
                    />
                    <label>Contraseña</label>
                    <input
                        type="password"
                        placeholder="Ingresa tu contraseña"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={styles.input}
                    />
                    <button type="submit" style={styles.btnPrimary}>
                        Iniciar Sesión
                    </button>
                </form>
                <button style={styles.btnSecondary} onClick={() => navigate('/register')}>
                    Registrarse
                </button>
                <a href="#" style={styles.forgot}>¿Olvidaste tu contraseña?</a>
                {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
            </div>
        </div>
    );
};

// Estilos en línea (puedes moverlos a un archivo CSS si prefieres)
const styles = {
    body: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f5f5ff',
    },
    container: {
        background: '#f0f0ff',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        width: '300px',
    },
    h2: {
        marginBottom: '20px',
    },
    input: {
        width: '100%',
        padding: '10px',
        margin: '10px 0',
        border: '1px solid #ccc',
        borderRadius: '5px',
    },
    btnPrimary: {
        width: '100%',
        padding: '10px',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        cursor: 'pointer',
        fontWeight: 'bold',
        backgroundColor: '#5555ff',
    },
    btnSecondary: {
        width: '100%',
        padding: '10px',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        cursor: 'pointer',
        fontWeight: 'bold',
        backgroundColor: '#000',
        marginTop: '10px',
    },
    forgot: {
        marginTop: '10px',
        display: 'block',
        color: '#333',
        textDecoration: 'none',
    },
};

export default Login;