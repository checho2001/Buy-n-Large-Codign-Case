const API_URL = 'http://127.0.0.1:8000/';

export const getTableData = async () => {
    try {
        const response = await fetch(`${API_URL}metrics/v1/table_data/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener datos de tabla');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener datos de tabla:', error);
        throw error;
    }
};

export const getGraphicsData = async () => {
    try {
        const response = await fetch(`${API_URL}metrics/v1/graphics_data/`, {
            method: 'GET', 
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener datos de gráficos');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener datos de gráficos:', error);
        throw error;
    }
};

export const getKPIData = async () => {
    try {
        const response = await fetch(`${API_URL}metrics/v1/kpi_data/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json', 
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener datos de KPI');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener datos de KPI:', error);
        throw error;
    }
};
