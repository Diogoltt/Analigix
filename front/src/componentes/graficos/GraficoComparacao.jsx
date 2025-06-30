import React, { useState, useEffect } from "react";
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
} from 'recharts';
import { buscarEstado } from "../../util/Estados"; // Não esqueça de importar corretamente

const formatarValorCompleto = (valor) => {
    if (!valor) return 'R$ 0';
    if (valor >= 1e9) return `R$ ${(valor / 1e9).toFixed(2)} bi`;
    if (valor >= 1e6) return `R$ ${(valor / 1e6).toFixed(2)} mi`;
    if (valor >= 1e3) return `R$ ${(valor / 1e3).toFixed(1)} mil`;
    return `R$ ${valor.toFixed(2)}`;
};

const formatarLabelCondicional = (valor) => {
    if (!valor || valor < 100000000) return '';
    if (valor >= 1e9) return `${(valor / 1e9).toFixed(1)}bi`;
    if (valor >= 1e6) return `${(valor / 1e6).toFixed(1)}mi`;
    return "";
};

const CATEGORIAS_DE_INTERESSE = [
    'Educação',
    'Saúde',
    'Tecnologia da Informação e Inovação',
    'Segurança Pública'
];

export default function GraficoComparacao({ ufA, ufB }) {
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!ufA || !ufB || ufA.toUpperCase() === ufB.toUpperCase()) {
            setLoading(false);
            setChartData([]);
            return;
        }

        const fetchDataForComparison = async () => {
            setLoading(true);
            const urlA = `http://127.0.0.1:5000/api/ranking?uf=${ufA}&per_page=50`;
            const urlB = `http://127.0.0.1:5000/api/ranking?uf=${ufB}&per_page=50`;

            try {
                const [responseA, responseB] = await Promise.all([fetch(urlA), fetch(urlB)]);
                const resultA = await responseA.json();
                const resultB = await responseB.json();

                if (resultA.error) throw new Error(`Erro na API para ${ufA}: ${resultA.error}`);
                if (resultB.error) throw new Error(`Erro na API para ${ufB}: ${resultB.error}`);

                const dataA = resultA.dados || [];
                const dataB = resultB.dados || [];

                const mergedDataMap = {};

                CATEGORIAS_DE_INTERESSE.forEach(cat => {
                    mergedDataMap[cat] = { categoria: cat, [ufA]: 0, [ufB]: 0 };
                });

                dataA.forEach(item => {
                    if (CATEGORIAS_DE_INTERESSE.includes(item.categoria_padronizada)) {
                        mergedDataMap[item.categoria_padronizada][ufA] = item.total_gasto;
                    }
                });

                dataB.forEach(item => {
                    if (CATEGORIAS_DE_INTERESSE.includes(item.categoria_padronizada)) {
                        mergedDataMap[item.categoria_padronizada][ufB] = item.total_gasto;
                    }
                });

                setChartData(Object.values(mergedDataMap));

            } catch (error) {
                console.error("Erro ao buscar dados para o gráfico de comparação:", error);
                setChartData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForComparison();
    }, [ufA, ufB]);

    const nomeEstadoA = buscarEstado(ufA)?.nome || ufA;
    const nomeEstadoB = buscarEstado(ufB)?.nome || ufB;

    return (
        <div style={{ width: "100%", height: 400 }}>
            <h2 style={{ textAlign: "center", color: "#5B228D" }}>
                Comparativo: {nomeEstadoA} vs {nomeEstadoB}
            </h2>
            <ResponsiveContainer width="100%" height="100%">
                {loading ? (
                    <p style={{ textAlign: 'center' }}>Carregando...</p>
                ) : chartData.length === 0 ? (
                    <p style={{ textAlign: 'center' }}>Não há dados para comparar ou selecione dois estados diferentes.</p>
                ) : (
                    <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 20, right: 150, left: 20, bottom: 20 }} // Aumentado para dar espaço aos rótulos
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            type="number"
                            tickFormatter={(v) => formatarValorCompleto(v).replace('R$ ', '')}
                        />
                        <YAxis
                            dataKey="categoria"
                            type="category"
                            width={180}
                            tick={{ fontSize: 12 }}
                        />
                        <Tooltip formatter={formatarValorCompleto} />
                        <Legend verticalAlign="top" />

                        <Bar dataKey={ufA} name={`Invest. ${ufA}`} fill="#0EC0D1">
                            <LabelList
                                dataKey={ufA}
                                position="right"
                                formatter={formatarLabelCondicional}
                                style={{ fill: '#333', fontSize: 12, whiteSpace: 'nowrap' }}
                                dx={8}
                            />
                        </Bar>

                        <Bar dataKey={ufB} name={`Invest. ${ufB}`} fill="#FFCC4D">
                            <LabelList
                                dataKey={ufB}
                                position="right"
                                formatter={formatarLabelCondicional}
                                style={{ fill: '#333', fontSize: 12, whiteSpace: 'nowrap' }}
                                dx={8}
                            />
                        </Bar>
                    </BarChart>
                )}
            </ResponsiveContainer>
        </div>
    );
}
