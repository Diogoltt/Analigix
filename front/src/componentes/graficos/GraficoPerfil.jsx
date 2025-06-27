import React from "react";
import './GraficoPerfil.css';

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';

export default function GraficoTeste({ chartData }) {
  const processedData = React.useMemo(() => {
    if (!chartData || chartData.length === 0) {
      return [];
    }
  
    const top5Data = chartData.slice(0, 5);

    const maxGasto = Math.max(...top5Data.map((item) => item.total_gasto));

    return top5Data.map((item) => ({
      area: item.categoria_padronizada,

      valor: (item.total_gasto / maxGasto) * 100,

      valorReal: item.total_gasto,
    }));
  }, [chartData]);

  return (
    <div className="radar-container">
      <h2 className="radar-title">Perfil de Investimentos</h2>
      <div className="radar-chart-wrapper">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={processedData}>
            <PolarGrid stroke="#ccc" />
            <PolarAngleAxis dataKey="area" stroke="#333" fontSize={12} />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 100]}
              stroke="transparent"
              tick={false}
            />
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
