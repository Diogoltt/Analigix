import React from "react";
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

// Dados fictícios dos 27 estados (investimento em bilhões, por exemplo)
const data = [
  { estado: "SP", investimento: 45.2 },
  { estado: "RJ", investimento: 32.8 },
  { estado: "MG", investimento: 30.1 },
  { estado: "RS", investimento: 28.7 },
  { estado: "PR", investimento: 26.4 },
  { estado: "SC", investimento: 25.0 },
  { estado: "BA", investimento: 23.9 },
  { estado: "PE", investimento: 20.4 },
  { estado: "CE", investimento: 19.2 },
  { estado: "GO", investimento: 17.8 },
  { estado: "MA", investimento: 16.5 },
  { estado: "PB", investimento: 15.1 },
  { estado: "PA", investimento: 14.3 },
  { estado: "RN", investimento: 13.2 },
  { estado: "PI", investimento: 12.8 },
  { estado: "AL", investimento: 11.7 },
  { estado: "MT", investimento: 11.3 },
  { estado: "MS", investimento: 10.6 },
  { estado: "SE", investimento: 10.2 },
  { estado: "ES", investimento: 9.9 },
  { estado: "AM", investimento: 9.4 },
  { estado: "RO", investimento: 8.8 },
  { estado: "TO", investimento: 8.2 },
  { estado: "AC", investimento: 7.5 },
  { estado: "RR", investimento: 7.2 },
  { estado: "AP", investimento: 6.8 },
  { estado: "DF", investimento: 6.3 },
];

export default function GraficoBarrasEstados() {
  return (
    <div className="grafico-container">
      <h2 className="barras-title">Comparação dos 27 Estados em números</h2>

      
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 40, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <YAxis type="number" label={{ value: "R$ (bilhões", angle: -90, position: "insideLeft", offset: 20 }} />
            <XAxis dataKey="estado" type="category" width={40} />
            <Tooltip formatter={(value) => `R$ ${value} bi`} />
            <Legend />
            <Bar dataKey="investimento" fill="#0EC0D1" name="Investimento" />
          </BarChart>
        </ResponsiveContainer>
      </div>
  );
}
