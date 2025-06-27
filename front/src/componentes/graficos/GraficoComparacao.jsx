import React from "react";
import { buscarEstado } from "../../util/Estados";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList,
} from "recharts";

const data = [
  {
    categoria: "Educação",
    estadoA: 60,
    estadoB: 80,
  },
  {
    categoria: "Saúde",
    estadoA: 75,
    estadoB: 90,
  },
  {
    categoria: "Infraestrutura",
    estadoA: 45,
    estadoB: 60,
  },
  {
    categoria: "Tecnologia",
    estadoA: 50,
    estadoB: 55,
  },
  {
    categoria: "Habitação",
    estadoA: 40,
    estadoB: 35,
  },
];

export default function GraficoComparacao({ ufA = "MS", ufB = "SP" }) {
  
  return (
    <div style={{ width: "100%", height: 500 }}>
      <h2 style={{ textAlign: "center", color: "#5B228D" }}>
        Comparativo de investimento entre os estados {ufA} e {ufB} (categorias)
      </h2>

      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 20, right: 40, left: 40, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis
            dataKey="categoria"
            type="category"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 14}}
          />
          <Tooltip formatter={(value) => `${value} milhões`} />
          <Legend verticalAlign="middle" align="left" layout="vertical" wrapperStyle={{ left: 0, top: 100, paddingRight: 60 }} />

          <Bar
            dataKey={(entry) => entry.estadoA}
            name={`Investimento - ${ufA}`}
            fill="#0EC0D1"
            isAnimationActive={false}
          >
            <LabelList dataKey={(entry) => -entry.estadoA} position="insideLeft" formatter={(v) => `${Math.abs(v)}`} style={{ fill: "#ffffff" }}/>
          </Bar>

          {/* Estado B */}
          <Bar
            dataKey="estadoB"
            name={`Investimento - ${ufB}`}
            fill="#FFCC4D"
            isAnimationActive={false}
          >
            <LabelList dataKey="estadoB" position="insideLeft" />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
