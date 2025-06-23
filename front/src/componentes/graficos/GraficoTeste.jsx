import React, { useMemo } from 'react'; // Importamos o useMemo para otimização
import './GraficoTeste.css';

import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer,
} from "recharts";

// O nome do seu componente agora recebe 'chartData' como propriedade
export default function GraficoTeste({ chartData }) {

    // Usamos useMemo para processar os dados. Este cálculo só será refeito se 'chartData' mudar.
    const processedData = useMemo(() => {
        // Se não houver dados, retorna um array vazio
        if (!chartData || chartData.length === 0) {
            return [];
        }

        // 1. Pega apenas as 5 categorias de maior investimento para o gráfico não ficar muito poluído
        const top5Data = chartData.slice(0, 5);

        // 2. Encontra o maior valor de gasto entre os top 5
        //    Usamos Math.max para encontrar o maior 'total_gasto'
        const maxGasto = Math.max(...top5Data.map(item => item.total_gasto));

        // 3. Normaliza os dados: Transforma os valores para uma escala de 0 a 100
        //    Isso garante que o maior investimento sempre ocupe 100% do eixo no gráfico.
        return top5Data.map(item => ({
            // O gráfico espera uma chave 'area', então renomeamos 'categoria_padronizada'
            area: item.categoria_padronizada,
            // O gráfico espera uma chave 'valor', então calculamos o valor normalizado
            valor: (item.total_gasto / maxGasto) * 100,
            // Guardamos o valor real para talvez usar em um tooltip no futuro
            valorReal: item.total_gasto 
        }));

    }, [chartData]); // A dependência é 'chartData'

    return (
        <div className="radar-container">
            {/* O título pode ser dinâmico também, mas vamos manter simples por enquanto */}
            <h2 className="radar-title">Perfil de Investimentos</h2>
            <div className="radar-chart-wrapper">
                <ResponsiveContainer width="100%" height="100%">
                    {/* O gráfico agora usa os dados processados e normalizados */}
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={processedData}>
                        <PolarGrid stroke="#ccc" />
                        <PolarAngleAxis dataKey="area" stroke="#333" fontSize={12} />
                        {/* O eixo de raio agora vai de 0 a 100, representando a porcentagem */}
                        <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="transparent" tick={false} />
                        <Radar
                            name="Investimentos"
                            dataKey="valor"
                            stroke="#14b8a6"
                            fill="#14b8a6"
                            fillOpacity={0.6}
                        />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}