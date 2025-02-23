import React, { useState, useEffect } from 'react';
import { getKPIData } from '../services/metricsInformation';
import { Card, Row, Col, Typography } from 'antd';

const { Title } = Typography;

const Dashboard = () => {
    const [kpiData, setKpiData] = useState({
        valor_inventario_total: 0,
        productos_stock_bajo: 0,
        productos_agotados: 0,
        productos_nuevos_mes_actual: 0
    });

    useEffect(() => {
        const fetchKPIData = async () => {
            try {
                const data = await getKPIData();
                setKpiData(data);
            } catch (error) {
                console.error('Error al cargar KPIs:', error);
            }
        };

        fetchKPIData();
    }, []);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'COP'
        }).format(value);
    };

    return (
        <div style={{ padding: '24px' }}>
            <Title level={2}>Panel de Control</Title>
            
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Title level={4}>Valor Total del Inventario</Title>
                        <Title level={3} style={{ color: '#1890ff' }}>
                            {formatCurrency(kpiData.valor_inventario_total)}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Title level={4}>Productos con Stock Bajo</Title>
                        <Title level={3} style={{ color: '#faad14' }}>
                            {kpiData.productos_stock_bajo}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Title level={4}>Productos Agotados</Title>
                        <Title level={3} style={{ color: '#ff4d4f' }}>
                            {kpiData.productos_agotados}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Title level={4}>Productos Nuevos este Mes</Title>
                        <Title level={3} style={{ color: '#52c41a' }}>
                            {kpiData.productos_nuevos_mes_actual}
                        </Title>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Dashboard;
