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
import { buscarEstado } from "../../util/Estados"; 
import './GraficoComparacao.css';

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


const calcularMetricas = (data, ufA, ufB) => {
    let totalA = 0, totalB = 0;
    let maiorDiferenca = { categoria: '', valor: 0, favorito: '' };
    let categoriaLiderA = { categoria: '', valor: 0 };
    let categoriaLiderB = { categoria: '', valor: 0 };

    data.forEach(item => {
        const valorA = item[ufA] || 0;
        const valorB = item[ufB] || 0;

        totalA += valorA;
        totalB += valorB;

        
        const diferenca = Math.abs(valorA - valorB);
        if (diferenca > maiorDiferenca.valor) {
            maiorDiferenca = {
                categoria: item.categoria,
                valor: diferenca,
                favorito: valorA > valorB ? ufA : ufB
            };
        }

        
        if (valorA > categoriaLiderA.valor) {
            categoriaLiderA = { categoria: item.categoria, valor: valorA };
        }
        if (valorB > categoriaLiderB.valor) {
            categoriaLiderB = { categoria: item.categoria, valor: valorB };
        }
    });

    const percentualSuperioridade = totalB > 0 ?
        ((Math.max(totalA, totalB) - Math.min(totalA, totalB)) / Math.min(totalA, totalB) * 100) : 0;

    return {
        totalA,
        totalB,
        maiorDiferenca,
        categoriaLiderA,
        categoriaLiderB,
        percentualSuperioridade: percentualSuperioridade.toFixed(1)
    };
};

export default function GraficoComparacao({ ufA, ufB, ano = 2024, onInsightGenerated, onCategoriasChange }) {
    const [chartData, setChartData] = useState([]);
    const [dadosCompletos, setDadosCompletos] = useState([]);
    const [categoriasSelecionadas, setCategoriasSelecionadas] = useState(new Set());
    const [loading, setLoading] = useState(true);

    const [metricas, setMetricas] = useState({
        totalA: 0,
        totalB: 0,
        maiorDiferenca: null,
        categoriaLiderA: null,
        categoriaLiderB: null,
        percentualSuperioridade: 0
    });

    useEffect(() => {
        if (!ufA || !ufB || ufA.toUpperCase() === ufB.toUpperCase()) {
            setLoading(false);
            setChartData([]);
            return;
        }

        const fetchDataForComparison = async () => {
            setLoading(true);
            const urlA = `http://127.0.0.1:5000/api/ranking?uf=${ufA}&ano=${ano}&per_page=50`;
            const urlB = `http://127.0.0.1:5000/api/ranking?uf=${ufB}&ano=${ano}&per_page=50`;

            try {
                const [responseA, responseB] = await Promise.all([fetch(urlA), fetch(urlB)]);
                const resultA = await responseA.json();
                const resultB = await responseB.json();

                if (resultA.error) throw new Error(`Erro na API para ${ufA}: ${resultA.error}`);
                if (resultB.error) throw new Error(`Erro na API para ${ufB}: ${resultB.error}`);

                const dataA = resultA.dados || [];
                const dataB = resultB.dados || [];

                const todasCategorias = new Map();

                [...dataA, ...dataB].forEach(item => {
                    const categoria = item.categoria_padronizada;
                    const valor = item.total_gasto || 0;
                    if (categoria && categoria !== 'Outros') {
                        if (todasCategorias.has(categoria)) {
                            todasCategorias.set(categoria, todasCategorias.get(categoria) + valor);
                        } else {
                            todasCategorias.set(categoria, valor);
                        }
                    }
                });

                const categoriasOrdenadas = Array.from(todasCategorias.entries())
                    .sort((a, b) => b[1] - a[1])
                    .map(([categoria, _]) => categoria);

                const mergedDataMap = {};

                categoriasOrdenadas.forEach(cat => {
                    mergedDataMap[cat] = { categoria: cat, [ufA]: 0, [ufB]: 0 };
                });

                dataA.forEach(item => {
                    if (item.categoria_padronizada && mergedDataMap[item.categoria_padronizada]) {
                        mergedDataMap[item.categoria_padronizada][ufA] = item.total_gasto;
                    }
                });

                dataB.forEach(item => {
                    if (item.categoria_padronizada && mergedDataMap[item.categoria_padronizada]) {
                        mergedDataMap[item.categoria_padronizada][ufB] = item.total_gasto;
                    }
                });

                const finalData = Object.values(mergedDataMap).sort((a, b) => {
                    const totalA = (a[ufA] || 0) + (a[ufB] || 0);
                    const totalB = (b[ufA] || 0) + (b[ufB] || 0);
                    return totalB - totalA;
                });

                setDadosCompletos(finalData);
                const topCategorias = finalData.slice(0, 8).map(item => item.categoria);
                setCategoriasSelecionadas(new Set(topCategorias));

            } catch (error) {
                console.error("Erro ao buscar dados para o gráfico de comparação:", error);
                setChartData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForComparison();
    }, [ufA, ufB, ano]);

    useEffect(() => {
        const dadosFiltrados = dadosCompletos.filter(item =>
            categoriasSelecionadas.has(item.categoria)
        );
        setChartData(dadosFiltrados);


        if (dadosFiltrados.length > 0) {
            const novasMetricas = calcularMetricas(dadosFiltrados, ufA, ufB);
            setMetricas(novasMetricas);
        }
    }, [dadosCompletos, categoriasSelecionadas, ufA, ufB]);

    useEffect(() => {
        if (onCategoriasChange && categoriasSelecionadas.size > 0) {
            onCategoriasChange(Array.from(categoriasSelecionadas));
        }
    }, [categoriasSelecionadas, onCategoriasChange]);

    const alternarCategoria = (nomeCategoria) => {
        const novaSelecao = new Set(categoriasSelecionadas);

        if (novaSelecao.has(nomeCategoria)) {
            novaSelecao.delete(nomeCategoria);
        } else if (novaSelecao.size < 8) {
            novaSelecao.add(nomeCategoria);
        }

        setCategoriasSelecionadas(novaSelecao);
    };

    const nomeEstadoA = buscarEstado(ufA)?.nome || ufA;
    const nomeEstadoB = buscarEstado(ufB)?.nome || ufB;

    return (
        <div style={{ width: "100%", height: "100%" }}>
            <div style={{ marginBottom: "1rem" }}>
                <h2 style={{ textAlign: "center", color: "#5B228D", marginBottom: "1rem" }}>
                    Comparativo: {nomeEstadoA} vs {nomeEstadoB}
                </h2>
                {!loading && dadosCompletos.length > 0 && (
                    <div style={{
                        marginBottom: '15px',
                        padding: '10px',
                        backgroundColor: '#f8f9fa',
                        borderRadius: '8px',
                        border: '1px solid #e9ecef'
                    }}>
                        <div style={{
                            fontSize: '0.9rem',
                            fontWeight: 'bold',
                            color: '#5B228D',
                            marginBottom: '8px'
                        }}>
                            Selecionar Categorias para Comparação (máx. 8):
                        </div>
                        <div style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            gap: '6px',
                            maxHeight: '150px',
                            overflowY: 'auto',
                            padding: '5px',
                            border: '1px solid #dee2e6',
                            borderRadius: '4px',
                            backgroundColor: '#fff'
                        }}>
                            {dadosCompletos.map((item) => (
                                <label
                                    key={item.categoria}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        cursor: 'pointer',
                                        fontSize: '0.8rem',
                                        padding: '4px 8px',
                                        backgroundColor: categoriasSelecionadas.has(item.categoria) ? '#e3f2fd' : '#fff',
                                        border: '1px solid #ddd',
                                        borderRadius: '4px',
                                        transition: 'all 0.2s ease'
                                    }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={categoriasSelecionadas.has(item.categoria)}
                                        onChange={() => alternarCategoria(item.categoria)}
                                        disabled={!categoriasSelecionadas.has(item.categoria) && categoriasSelecionadas.size >= 8}
                                        style={{ marginRight: '5px' }}
                                    />
                                    <span style={{
                                        color: categoriasSelecionadas.has(item.categoria) ? '#1976d2' : '#666',
                                        fontWeight: categoriasSelecionadas.has(item.categoria) ? 'bold' : 'normal'
                                    }}>
                                        {item.categoria}
                                    </span>
                                </label>
                            ))}
                        </div>
                        <div style={{
                            fontSize: '0.75rem',
                            color: '#666',
                            marginTop: '5px'
                        }}>
                            {categoriasSelecionadas.size}/8 categorias selecionadas
                        </div>
                    </div>
                )}

                {!loading && chartData.length > 0 && (
                    <div style={{
                        display: "flex",
                        justifyContent: "space-around",
                        marginBottom: "1rem",
                        padding: "0.8rem",
                        backgroundColor: "#f8f9fa",
                        borderRadius: "8px",
                        fontSize: "0.85rem"
                    }}>
                        <div style={{ textAlign: "center" }}>
                            <div style={{ fontWeight: "bold", color: "#0EC0D1" }}>
                                {formatarValorCompleto(metricas.totalA)}
                            </div>
                            <div style={{ fontSize: "0.75rem", color: "#666" }}>Total {ufA}</div>
                        </div>

                        <div style={{ textAlign: "center" }}>
                            <div style={{ fontWeight: "bold", color: "#FFCC4D" }}>
                                {formatarValorCompleto(metricas.totalB)}
                            </div>
                            <div style={{ fontSize: "0.75rem", color: "#666" }}>Total {ufB}</div>
                        </div>

                        {metricas.maiorDiferenca && (
                            <div style={{ textAlign: "center" }}>
                                <div style={{ fontWeight: "bold", color: "#e74c3c" }}>
                                    {metricas.percentualSuperioridade}%
                                </div>
                                <div style={{ fontSize: "0.75rem", color: "#666" }}>
                                    Diferença média
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <ResponsiveContainer width="100%" height={loading || chartData.length === 0 ? 200 : 500}>
                {loading ? (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%',
                        color: '#666'
                    }}>
                        Carregando dados de comparação...
                    </div>
                ) : chartData.length === 0 ? (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%',
                        color: '#666',
                        flexDirection: 'column'
                    }}>
                        <div>⚠️ Dados não disponíveis</div>
                        <div style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                            Selecione dois estados diferentes ou verifique a conexão
                        </div>
                    </div>
                ) : (
                    <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 20, right: 160, left: 20, bottom: 20 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            type="number"
                            tickFormatter={(v) => formatarValorCompleto(v).replace('R$ ', '')}
                        />
                        <YAxis
                            dataKey="categoria"
                            type="category"
                            width={200}
                            tick={{ fontSize: 11 }}
                        />
                        <Tooltip
                            formatter={(value, name) => [
                                formatarValorCompleto(value),
                                `Investimento ${name.replace('Invest. ', '')}`
                            ]}
                            labelStyle={{ color: '#333', fontSize: '12px' }}
                        />
                        <Legend verticalAlign="top" />

                        <Bar
                            dataKey={ufA}
                            name={`Invest. ${ufA}`}
                            fill="#0EC0D1"
                        >
                            <LabelList
                                dataKey={ufA}
                                position="right"
                                formatter={formatarLabelCondicional}
                                style={{ fill: '#333', fontSize: 11, whiteSpace: 'nowrap' }}
                                dx={8}
                            />
                        </Bar>

                        <Bar
                            dataKey={ufB}
                            name={`Invest. ${ufB}`}
                            fill="#FFCC4D"
                        >
                            <LabelList
                                dataKey={ufB}
                                position="right"
                                formatter={formatarLabelCondicional}
                                style={{ fill: '#333', fontSize: 11, whiteSpace: 'nowrap' }}
                                dx={8}
                            />
                        </Bar>
                    </BarChart>
                )}
            </ResponsiveContainer>
        </div>
    );
}
