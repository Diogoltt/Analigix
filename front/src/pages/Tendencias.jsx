import React, { useState, useEffect, useCallback } from 'react';
import './css/Tendencias.css';
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ESTADOS_BR } from '../util/Estados';

export default function Tendencias() {
    const [estadoSelecionado, setEstadoSelecionado] = useState('SP');
    const [categoriaSelecionada, setCategoriaSelecionada] = useState('');
    const [categorias, setCategorias] = useState([]);
    const [dadosTendencia, setDadosTendencia] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Buscar categorias disponíveis
    useEffect(() => {
        const fetchCategorias = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/categorias');
                if (!response.ok) {
                    throw new Error('Erro ao buscar categorias');
                }
                const data = await response.json();
                setCategorias(data || []);
                if (data && data.length > 0) {
                    setCategoriaSelecionada(data[0]);
                }
            } catch (error) {
                console.error('Erro ao buscar categorias:', error);
                setError('Erro ao carregar categorias');
            }
        };

        fetchCategorias();
    }, []);

    const fetchDadosTendencia = useCallback(async () => {
        setLoading(true);
        setError(null);
        
        try {
            const anos = [2020, 2021, 2022, 2023, 2024, 2025];
            const dadosPromises = anos.map(async (ano) => {
                try {
                    const response = await fetch(`http://localhost:5000/api/despesas-estado/${estadoSelecionado}/${ano}`);
                    if (!response.ok) {
                        return { ano, valor: 0 };
                    }
                    const data = await response.json();
                    
                    // Encontrar o valor para a categoria selecionada
                    const categoriaData = data.find(item => item.categoria === categoriaSelecionada);
                    const valor = categoriaData ? parseFloat(categoriaData.valor) : 0;
                    
                    return { ano, valor };
                } catch (error) {
                    console.warn(`Erro ao buscar dados para ${ano}:`, error);
                    return { ano, valor: 0 };
                }
            });

            const resultados = await Promise.all(dadosPromises);
            setDadosTendencia(resultados);
        } catch (error) {
            console.error('Erro ao buscar dados de tendência:', error);
            setError('Erro ao carregar dados de tendência');
        } finally {
            setLoading(false);
        }
    }, [estadoSelecionado, categoriaSelecionada]);

    // Buscar dados de tendência quando estado ou categoria mudam
    useEffect(() => {
        if (estadoSelecionado && categoriaSelecionada) {
            fetchDadosTendencia();
        }
    }, [estadoSelecionado, categoriaSelecionada, fetchDadosTendencia]);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value);
    };

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-label">{`Ano: ${label}`}</p>
                    <p className="tooltip-value">
                        {`Despesas: ${formatCurrency(payload[0].value)}`}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="tendencias-container">
            <nav className="navbar">
                <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
                <div className="nav-links">
                    <a href="/nacional" style={{ color: "white" }}>Dashboard</a>
                    <a href="/portais-da-Transparencia" style={{ color: "white" }}>Portal da Transparência</a>
                </div>
            </nav>

            <div className="tendencias-content">
                <div className="header-section">
                    <h1>Análise de Tendências</h1>
                    <p>Acompanhe a evolução das despesas por estado e categoria ao longo dos anos</p>
                </div>

                <div className="filtros-container">
                    <div className="filtro-grupo">
                        <label htmlFor="estado-select">Estado:</label>
                        <select
                            id="estado-select"
                            value={estadoSelecionado}
                            onChange={(e) => setEstadoSelecionado(e.target.value)}
                            className="filtro-select"
                        >
                            {Object.entries(ESTADOS_BR).map(([nome, uf]) => (
                                <option key={uf} value={uf}>
                                    {nome} ({uf})
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="filtro-grupo">
                        <label htmlFor="categoria-select">Categoria:</label>
                        <select
                            id="categoria-select"
                            value={categoriaSelecionada}
                            onChange={(e) => setCategoriaSelecionada(e.target.value)}
                            className="filtro-select"
                        >
                            {categorias.map((categoria) => (
                                <option key={categoria} value={categoria}>
                                    {categoria}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="grafico-container">
                    {loading && (
                        <div className="loading">
                            <p>Carregando dados de tendência...</p>
                        </div>
                    )}

                    {error && (
                        <div className="error">
                            <p>{error}</p>
                        </div>
                    )}

                    {!loading && !error && dadosTendencia.length > 0 && (
                        <div className="chart-wrapper">
                            <h2>
                                Evolução de Despesas - {categoriaSelecionada}
                                <br />
                                <span className="estado-nome">
                                    {Object.keys(ESTADOS_BR).find(nome => ESTADOS_BR[nome] === estadoSelecionado)} ({estadoSelecionado})
                                </span>
                            </h2>
                            
                            <ResponsiveContainer width="100%" height={400}>
                                <LineChart
                                    data={dadosTendencia}
                                    margin={{
                                        top: 20,
                                        right: 30,
                                        left: 20,
                                        bottom: 5,
                                    }}
                                >
                                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                                    <XAxis 
                                        dataKey="ano" 
                                        stroke="#666"
                                        fontSize={12}
                                    />
                                    <YAxis 
                                        stroke="#666"
                                        fontSize={12}
                                        tickFormatter={(value) => {
                                            if (value >= 1000000000) {
                                                return `R$ ${(value / 1000000000).toFixed(1)}B`;
                                            } else if (value >= 1000000) {
                                                return `R$ ${(value / 1000000).toFixed(1)}M`;
                                            } else if (value >= 1000) {
                                                return `R$ ${(value / 1000).toFixed(1)}K`;
                                            }
                                            return `R$ ${value}`;
                                        }}
                                    />
                                    <Tooltip content={<CustomTooltip />} />
                                    <Legend />
                                    <Line 
                                        type="monotone" 
                                        dataKey="valor" 
                                        stroke="#0EC0D1" 
                                        strokeWidth={3}
                                        dot={{ fill: '#0EC0D1', strokeWidth: 2, r: 6 }}
                                        activeDot={{ r: 8, stroke: '#5B228D', strokeWidth: 2 }}
                                        name="Despesas (R$)"
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    )}

                    {!loading && !error && dadosTendencia.length === 0 && (
                        <div className="no-data">
                            <p>Nenhum dado encontrado para os filtros selecionados.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
