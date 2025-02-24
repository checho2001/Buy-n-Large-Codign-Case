import React, { useState, useEffect } from 'react';
import { getKPIData, getTableData, getGraphicsData } from '../services/metricsInformation';
import { Card, Row, Col, Typography, Table, Divider } from 'antd';
import { 
    PieChart, Pie, Cell, 
    Treemap,
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    LineChart, Line,
    AreaChart, Area,
    ResponsiveContainer 
} from 'recharts';

const { Title } = Typography;

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const Dashboard = () => {
    const [kpiData, setKpiData] = useState({
        valor_inventario_total: 0,
        productos_stock_bajo: 0,
        productos_agotados: 0,
        productos_nuevos_mes_actual: 0
    });
    const [tableData, setTableData] = useState({
        productos_stock_bajo: [],
        movimientos_recientes: [],
        combinaciones_caracteristicas: []
    });

    const [graphicsData, setGraphicsData] = useState({
        distribucion_stock: { labels: [], datos: [] },
        mapa_arbol: [],
        barras_agrupadas_features: { labels: [], datos: [] },
        linea_tiempo: { fechas: [], stock: [] },
        areas_apiladas: {}
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

    useEffect(() => {
        const fetchTableData = async () => {
            try {
                const data = await getTableData();
                setTableData(data);
            } catch (error) {
                console.error('Error al cargar datos de tablas:', error);
            }
        };

        fetchTableData();
    }, []);

    useEffect(() => {
        const fetchGraphicsData = async () => {
            try {
                const data = await getGraphicsData();
                setGraphicsData(data);
            } catch (error) {
                console.error('Error al cargar gráficos:', error);
            }
        };

        fetchGraphicsData();
    }, []);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'COP'
        }).format(value);
    };

    const stockBajoColumns = [
        { title: 'Producto', dataIndex: 'name', key: 'name' },
        { title: 'Categoría', dataIndex: 'category', key: 'category' },
        { title: 'Marca', dataIndex: 'brand', key: 'brand' },
        { 
            title: 'Stock', 
            dataIndex: 'stock', 
            key: 'stock',
            render: (stock) => (
                <span style={{ color: stock < 5 ? '#ff4d4f' : '#faad14' }}>
                    {stock}
                </span>
            )
        },
    ];

    const movimientosColumns = [
        { title: 'Producto', dataIndex: 'name', key: 'name' },
        { title: 'Categoría', dataIndex: 'category', key: 'category' },
        { title: 'Stock Actual', dataIndex: 'stock', key: 'stock' },
        { title: 'Última Actualización', dataIndex: 'updated_at', key: 'updated_at' },
    ];

    const caracteristicasColumns = [
        { 
            title: 'Características', 
            dataIndex: 'combinacion', 
            key: 'combinacion',
            render: (text) => (
                <span style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {text}
                </span>
            )
        },
        { 
            title: 'Stock Total', 
            dataIndex: 'stock_total', 
            key: 'stock_total',
            sorter: (a, b) => a.stock_total - b.stock_total,
        },
    ];

    // Transformar datos para gráfica de dona
    const pieData = graphicsData.distribucion_stock.labels.map((label, index) => ({
        name: label,
        value: graphicsData.distribucion_stock.datos[index]
    }));

    // Transformar datos para gráfica de barras agrupadas
    const barData = graphicsData.barras_agrupadas_features.labels.map((label, index) => ({
        name: label,
        stock: graphicsData.barras_agrupadas_features.datos[index]
    }));

    // Transformar datos para línea de tiempo
    const lineData = graphicsData.linea_tiempo.fechas.map((fecha, index) => ({
        fecha: fecha,
        stock: graphicsData.linea_tiempo.stock[index]
    }));

    // Transformar datos para áreas apiladas
    const areaData = graphicsData.areas_apiladas.fechas?.map((fecha, index) => {
        const dataPoint = { fecha };
        Object.keys(graphicsData.areas_apiladas).forEach(key => {
            if (key !== 'fechas') {
                dataPoint[key] = graphicsData.areas_apiladas[key][index];
            }
        });
        return dataPoint;
    }) || [];

    return (
        <div style={{ padding: '24px' }}>
            <Title style={{ marginBottom: '8px' }}>Dashboard y Métricas</Title>
            <Title level={3} style={{ 
                color: '#8c8c8c', 
                marginBottom: '32px',
                fontWeight: 'normal' 
            }}>
                Indicadores
            </Title>
            
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} lg={6}>
                    <Card hoverable>
                        <Title level={4} style={{ marginBottom: '16px' }}>
                            Valor Total del Inventario
                        </Title>
                        <Title level={3} style={{ 
                            color: '#1890ff',
                            margin: 0
                        }}>
                            {formatCurrency(kpiData.valor_inventario_total)}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card hoverable>
                        <Title level={4} style={{ marginBottom: '16px' }}>
                            Productos con Stock Bajo
                        </Title>
                        <Title level={3} style={{ 
                            color: '#faad14',
                            margin: 0
                        }}>
                            {kpiData.productos_stock_bajo}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card hoverable>
                        <Title level={4} style={{ marginBottom: '16px' }}>
                            Productos Agotados
                        </Title>
                        <Title level={3} style={{ 
                            color: '#ff4d4f',
                            margin: 0
                        }}>
                            {kpiData.productos_agotados}
                        </Title>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card hoverable>
                        <Title level={4} style={{ marginBottom: '16px' }}>
                            Productos Nuevos este Mes
                        </Title>
                        <Title level={3} style={{ 
                            color: '#52c41a',
                            margin: 0
                        }}>
                            {kpiData.productos_nuevos_mes_actual}
                        </Title>
                    </Card>
                </Col>
            </Row>

            <Divider />

            <Title level={3} style={{ 
                color: '#8c8c8c', 
                marginBottom: '32px',
                fontWeight: 'normal' 
            }}>
                Tablas
            </Title>

            <Row gutter={[16, 16]}>
                <Col span={24}>
                    <Card title="Top 5 Productos con Menor Stock" bordered={false}>
                        <Table 
                            dataSource={tableData.productos_stock_bajo}
                            columns={stockBajoColumns}
                            pagination={false}
                            size="small"
                        />
                    </Card>
                </Col>

                <Col span={24}>
                    <Card title="Últimos Movimientos de Inventario" bordered={false}>
                        <Table 
                            dataSource={tableData.movimientos_recientes}
                            columns={movimientosColumns}
                            pagination={false}
                            size="small"
                        />
                    </Card>
                </Col>

                <Col span={24}>
                    <Card title="Ranking de Características con Mayor Stock" bordered={false}>
                        <Table 
                            dataSource={tableData.combinaciones_caracteristicas}
                            columns={caracteristicasColumns}
                            pagination={false}
                            size="small"
                        />
                    </Card>
                </Col>
            </Row>

            <Divider />

            <Title level={3} style={{ 
                color: '#8c8c8c', 
                marginBottom: '32px',
                fontWeight: 'normal' 
            }}>
                Gráficas
            </Title>

            <Row gutter={[16, 16]}>
                {/* Distribución por Categoría */}
                <Col xs={24} lg={12}>
                    <Card title="Distribución por Categoría" bordered={false}>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    dataKey="value"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={80}
                                    label
                                >
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </Card>
                </Col>

                {/* Mapa de Árbol */}
                <Col xs={24} lg={12}>
                    <Card title="Jerarquía Brand > Categoría" bordered={false}>
                        <ResponsiveContainer width="100%" height={300}>
                            <Treemap
                                data={graphicsData.mapa_arbol}
                                dataKey="value"
                                nameKey="name"
                                aspectRatio={4/3}
                            >
                                <Tooltip />
                            </Treemap>
                        </ResponsiveContainer>
                    </Card>
                </Col>

                {/* Características Técnicas */}
                <Col xs={24}>
                    <Card title="Stock por Combinación de Características" bordered={false}>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={barData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="stock" fill="#8884d8" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Card>
                </Col>

                {/* Evolución Temporal */}
                <Col xs={24} lg={12}>
                    <Card title="Tendencia de Stock Total" bordered={false}>
                        <ResponsiveContainer width="100%" height={300}>
                            <LineChart data={lineData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="fecha" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="stock" stroke="#8884d8" />
                            </LineChart>
                        </ResponsiveContainer>
                    </Card>
                </Col>

                {/* Áreas Apiladas */}
                <Col xs={24} lg={12}>
                    <Card title="Stock por Categoría en el Tiempo" bordered={false}>
                        <ResponsiveContainer width="100%" height={300}>
                            <AreaChart data={areaData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="fecha" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                {Object.keys(graphicsData.areas_apiladas).map((key, index) => (
                                    key !== 'fechas' && (
                                        <Area 
                                            key={key}
                                            type="monotone" 
                                            dataKey={key} 
                                            stackId="1"
                                            fill={COLORS[index % COLORS.length]}
                                            stroke={COLORS[index % COLORS.length]}
                                        />
                                    )
                                ))}
                            </AreaChart>
                        </ResponsiveContainer>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Dashboard;
