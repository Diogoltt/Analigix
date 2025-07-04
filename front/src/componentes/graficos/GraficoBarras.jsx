import React, { useState, useEffect } from "react";
import "./GraficoBarras.css";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
    Legend,
} from "recharts";

//
const formatarNumero = (num) => {
    if (!num) return 'R$ 0';
    if (num >= 1e12) { 
        return `R$ ${(num / 1e12).toFixed(2)} tri`;
    }
    if (num >= 1e9) { 
        return `R$ ${(num / 1e9).toFixed(2)} bi`;
    }
    if (num >= 1e6) { 
        return `R$ ${(num / 1e6).toFixed(2)} mi`;
    }
    if (num >= 1e3) { 
        return `R$ ${(num / 1e3).toFixed(1)} mil`;
    }
    return `R$ ${num.toFixed(2)}`;
};

export default function GraficoBarrasEstados({ ano = 2024 }) {
    const [categoriaSelecionada, setCategoriaSelecionada] = useState("");
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [categorias, setCategorias] = useState([]);
    const [estadosOcultos, setEstadosOcultos] = useState(new Set());
    const [dadosOriginais, setDadosOriginais] = useState([]);

    // Buscar categorias disponíveis
    useEffect(() => {
        const fetchCategorias = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/categorias');
                const data = await response.json();
                setCategorias(data);
            } catch (error) {
                console.error("Erro ao buscar categorias:", error);
                setCategorias([]);
            }
        };

        fetchCategorias();
    }, []);

    useEffect(() => {
        const fetchDataForChart = async () => {
            setLoading(true);
            let apiUrl = `http://127.0.0.1:5000/api/comparativo-geral?ano=${ano}`;

            if (categoriaSelecionada) {
                apiUrl += `&categoria=${encodeURIComponent(categoriaSelecionada)}`;
            }

            try {
                const response = await fetch(apiUrl);
                const data = await response.json();

                if (data.error) throw new Error(data.error);
                
                setDadosOriginais(data);
                
                // Filtrar estados ocultos
                const dadosFiltrados = data.filter(item => !estadosOcultos.has(item.estado));
                setChartData(dadosFiltrados);

            } catch (error) {
                console.error("Erro ao buscar dados para o gráfico:", error);
                setChartData([]);
                setDadosOriginais([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForChart();
    }, [categoriaSelecionada, ano, estadosOcultos]);

    // Função para alternar visibilidade do estado
    const toggleEstado = (estado) => {
        const novosEstadosOcultos = new Set(estadosOcultos);
        if (novosEstadosOcultos.has(estado)) {
            novosEstadosOcultos.delete(estado);
        } else {
            novosEstadosOcultos.add(estado);
        }
        setEstadosOcultos(novosEstadosOcultos);
    };

    return (
        <div className="grafico-container" style={{ minHeight: "500px" }}>
            <div className="controles-grafico">
                <div style={{ marginBottom: "15px" }}>
                    <label style={{ marginRight: "10px", fontWeight: "bold" }}>
                        Filtrar por Categoria:
                    </label>
                    <select
                        className="categoria-graficoBarras"
                        value={categoriaSelecionada}
                        onChange={(e) => setCategoriaSelecionada(e.target.value)}
                    >
                        <option value="">Geral (Todas as Categorias)</option>
                        {categorias.map(categoria => (
                            <option key={categoria} value={categoria}>
                                {categoria}
                            </option>
                        ))}
                    </select>
                </div>

                {dadosOriginais.length > 0 && (
                    <div>
                        <label style={{ marginBottom: "10px", fontWeight: "bold", display: "block" }}>
                            Ocultar Estados:
                        </label>
                        <div className="estados-checkbox-container">
                            {dadosOriginais.map(item => (
                                <label key={item.estado} className="estado-checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={estadosOcultos.has(item.estado)}
                                        onChange={() => toggleEstado(item.estado)}
                                    />
                                    {item.estado}
                                </label>
                            ))}
                        </div>
                        {estadosOcultos.size > 0 && (
                            <div className="info-estados-ocultos">
                                {estadosOcultos.size} estado{estadosOcultos.size > 1 ? 's' : ''} oculto{estadosOcultos.size > 1 ? 's' : ''}
                            </div>
                        )}
                    </div>
                )}
            </div>
            
            <h2 className="barras-title">
                {categoriaSelecionada
                    ? `Comparativo de Investimentos em ${categoriaSelecionada}`
                    : "Comparativo de Investimentos Totais por Estado"}
            </h2>

            <ResponsiveContainer width="100%" height={400}>
                {loading ? (
                    <p style={{textAlign: 'center'}}>Carregando...</p>
                ) : (
                    <BarChart data={chartData} margin={{ top: 20, right: 30, left: 80, bottom: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <YAxis 
                            type="number" 
                            dataKey="total_investido" 
                            tickFormatter={formatarNumero} 
                            width={100}
                        />

                        <XAxis dataKey="estado" type="category" interval={0} angle={-45} textAnchor="end" height={60} />
                        <Tooltip formatter={formatarNumero} />
                        
                        <Legend />
                        <Bar dataKey="total_investido" fill="#0EC0D1" name="Investimento" />
                    </BarChart>
                )}
            </ResponsiveContainer>
        </div>
    );
}