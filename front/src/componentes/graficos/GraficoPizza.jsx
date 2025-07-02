import React, { useState, useEffect } from 'react';
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip,
    Legend
} from 'recharts';
const CORES = [
    '#5B228D', '#0EC0D1', '#FFCC4D', '#e74c3c', '#27ae60',
    '#f39c12', '#9b59b6', '#34495e', '#e67e22', '#1abc9c',
    '#3498db', '#e91e63', '#ff5722', '#795548', '#607d8b'
];

const formatarValor = (valor) => {
    if (!valor) return 'R$ 0';
    if (valor >= 1e9) return `R$ ${(valor / 1e9).toFixed(2)} bi`;
    if (valor >= 1e6) return `R$ ${(valor / 1e6).toFixed(2)} mi`;
    if (valor >= 1e3) return `R$ ${(valor / 1e3).toFixed(1)} mil`;
    return `R$ ${valor.toFixed(2)}`;
};

const GraficoPizza = ({ uf, anoSelecionado }) => {
    const [dados, setDados] = useState([]);
    const [loading, setLoading] = useState(true);
    const [totalGeral, setTotalGeral] = useState(0);

    useEffect(() => {
        const buscarDadosPizza = async () => {
            if (!uf) return;

            setLoading(true);

            try {
                const params = new URLSearchParams();
                params.append('uf', uf);
                params.append('per_page', 10);
                if (anoSelecionado) params.append('ano', anoSelecionado);

                const url = `http://127.0.0.1:5000/api/ranking?${params.toString()}`;
                const response = await fetch(url);
                const resultado = await response.json();

                if (resultado.error) {
                    throw new Error(resultado.error);
                }

                const dadosRanking = resultado.dados || [];

                
                const total = dadosRanking.reduce((soma, item) => soma + (item.total_gasto || 0), 0);
                setTotalGeral(total);

                
                const dadosProcessados = dadosRanking
                    .filter(item => item.categoria_padronizada !== 'Outros') 
                    .map(item => ({
                        name: item.categoria_padronizada || 'Sem Categoria',
                        value: item.total_gasto || 0,
                        percentual: total > 0 ? ((item.total_gasto || 0) / total * 100).toFixed(1) : 0
                    }))
                    .filter(item => item.value > 0) 
                    .sort((a, b) => b.value - a.value) 
                    .slice(0, 8); 

                setDados(dadosProcessados);

            } catch (error) {
                console.error('Erro ao buscar dados para gráfico de pizza:', error);
                setDados([]);
            } finally {
                setLoading(false);
            }
        };

        buscarDadosPizza();
    }, [uf, anoSelecionado]);

    const renderTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div style={{
                    backgroundColor: '#fff',
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderRadius: '5px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                }}>
                    <p style={{ margin: 0, fontWeight: 'bold', color: '#333' }}>
                        {data.name}
                    </p>
                    <p style={{ margin: '5px 0 0 0', color: '#666' }}>
                        Valor: {formatarValor(data.value)}
                    </p>
                    <p style={{ margin: '5px 0 0 0', color: '#666' }}>
                        Participação: {data.percentual}%
                    </p>
                </div>
            );
        }
        return null;
    };

    const renderLabel = ({ percentual, name }) => {
        if (parseFloat(percentual) > 3) {
            return `${percentual}%`;
        }
        return '';
    };

    if (loading) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                color: '#666'
            }}>
                Carregando distribuição de despesas...
            </div>
        );
    }

    if (dados.length === 0) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                color: '#666',
                flexDirection: 'column'
            }}>
                <div>📊 Dados não disponíveis</div>
                <div style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    Não há dados de despesas para este estado/período
                </div>
            </div>
        );
    }

    return (
        <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{
                textAlign: 'center',
                color: '#5B228D',
                marginBottom: '10px',
                fontSize: '1.1rem'
            }}>
                Distribuição de Despesas - {uf}
            </h3>
            <div style={{
                textAlign: 'center',
                fontSize: '0.85rem',
                color: '#666',
                marginBottom: '15px'
            }}>
                Total: {formatarValor(totalGeral)} {anoSelecionado && `(${anoSelecionado})`}
            </div>

            <div style={{ flex: 1 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={dados}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={renderLabel}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                        >
                            {dados.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={CORES[index % CORES.length]}
                                />
                            ))}
                        </Pie>
                        <Tooltip content={renderTooltip} />
                        <Legend
                            wrapperStyle={{
                                fontSize: '10px',
                                lineHeight: '12px'
                            }}
                            iconType="square"
                        />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default GraficoPizza;
