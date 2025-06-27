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

export default function GraficoBarrasEstados() {
    const [categoriaSelecionada, setCategoriaSelecionada] = useState("");
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // --- DEBUG PONTO 1: O useEffect foi acionado? ---
        console.log(`[DEBUG-GRAFICO] useEffect disparado. Categoria agora é: '${categoriaSelecionada}'`);

        if (!categoriaSelecionada) {
            setChartData([]); // Limpa os dados se nenhuma categoria for selecionada
            return; // Para a execução aqui
        }

        const fetchDataForChart = async () => {
            setLoading(true);
            try {
                const apiUrl = `http://127.0.0.1:5000/api/comparativo-nacional?categoria=${categoriaSelecionada}`;
                
                // --- DEBUG PONTO 2: A URL está correta? ---
                console.log(`[DEBUG-GRAFICO] Buscando dados na URL: ${apiUrl}`);

                const response = await fetch(apiUrl);
                const data = await response.json();

                // --- DEBUG PONTO 3: O que a API realmente retornou? ---
                // Esta é a linha mais importante.
                console.log("[DEBUG-GRAFICO] Dados brutos recebidos da API:", data);

                // Verifica se a API não retornou um erro
                if (data.error) {
                    throw new Error(data.error);
                }

                // Converte os valores para milhões
                const dataInMillions = data.map(item => ({
                    ...item,
                    total_investido: item.total_investido / 1000000 
                }));
                
                // --- DEBUG PONTO 4: Os dados foram processados corretamente? ---
                console.log("[DEBUG-GRAFICO] Dados processados (em milhões):", dataInMillions);

                setChartData(dataInMillions);

            } catch (error) {
                // --- DEBUG PONTO 5: Aconteceu algum erro no processo? ---
                console.error("[DEBUG-GRAFICO] Falha na busca ou processamento:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForChart();
    }, [categoriaSelecionada]);

    const handleCategoriaChange = (e) => {
        setCategoriaSelecionada(e.target.value);
    };
    
    // --- DEBUG PONTO 6: Qual o estado final dos dados antes de renderizar? ---
    console.log("[DEBUG-GRAFICO] Estado 'chartData' antes do return:", chartData);

    return (
        <div className="grafico-container" style={{ minHeight: "500px" }}>
            <select
                id="categoria-select"
                className="categoria-graficoBarras"
                value={categoriaSelecionada}
                onChange={handleCategoriaChange}
            >
                <option value="" disabled>Selecione a Categoria</option>
                <option value="EDUCACAO">Educação</option>
                <option value="SAUDE">Saúde</option>
                <option value="ADMINISTRACAO">Administração</option>
                <option value="TRANSPORTE">Transporte</option>
                <option value="SEGURANCA PUBLICA">Segurança Pública</option>
            </select>
            
            <h2 className="barras-title">
                {categoriaSelecionada
                    ? `Comparação de Investimentos em ${categoriaSelecionada}`
                    : "Selecione uma categoria para visualizar o gráfico"}
            </h2>

            <ResponsiveContainer width="100%" height={400}>
                {loading ? (
                    <p style={{textAlign: 'center'}}>Carregando dados...</p>
                ) : chartData.length > 0 ? (
                    <BarChart data={chartData} /* ... */ >
                        <CartesianGrid strokeDasharray="3 3" />
                        <YAxis type="number" label={{ value: "R$ (milhões)", angle: -90, position: "insideLeft" }} />
                        <XAxis dataKey="estado" type="category" interval={0} angle={-45} textAnchor="end" height={60} />
                        <Tooltip formatter={(value) => `R$ ${value.toFixed(2)} mi`} />
                        <Legend />
                        <Bar dataKey="total_investido" fill="#0EC0D1" name="Investimento" />
                    </BarChart>
                ) : (
                    <p style={{textAlign: 'center'}}>Sem dados para exibir para esta categoria.</p>
                )}
            </ResponsiveContainer>
        </div>
    );
}