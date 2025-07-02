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
                
                
                setChartData(data);

            } catch (error) {
                console.error("Erro ao buscar dados para o gráfico:", error);
                setChartData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForChart();
    }, [categoriaSelecionada, ano]);

    return (
        <div className="grafico-container" style={{ minHeight: "500px" }}>
            <select
                className="categoria-graficoBarras"
                value={categoriaSelecionada}
                onChange={(e) => setCategoriaSelecionada(e.target.value)}
            >
                <option value="">Geral (Todas as Categorias)</option>
                <option value="Educação">Educação</option>
                <option value="Saúde">Saúde</option>
                <option value="Segurança Pública">Segurança Pública</option>
                <option value="Infraestrutura e Transporte">Infraestrutura e Transporte</option>
                <option value="Administração e Gestão Pública">Administração e Gestão Pública</option>
                <option value="Tecnologia da Informação e Inovação">Tecnologia da Informação e Inovação</option>

            </select>
            
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