import React from "react";
import './GraficoTeste.css';

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

const data = [
  { area: "Educação", valor: 85 },
  { area: "Saúde", valor: 78 },
  { area: "Habitação", valor: 60 },
  { area: "Infraestrutura", valor: 55 },
  { area: "Segurança", valor: 50 },
];

export default function RadarChartMS() {
  return (
    <div className="radar-container">
      <h2 className="radar-title">Perfil de Investimentos – MS (2025)</h2>
      <div className="radar-chart-wrapper">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid stroke="#ccc" />
            <PolarAngleAxis dataKey="area" stroke="#333" fontSize={12} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#aaa" tick={{ fontSize: 10 }} />
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
