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
    'Segurança Pública',
    'Infraestrutura e Transporte',
    'Administração e Gestão Pública',
    'Fazenda e Finanças',
    'Meio Ambiente'
];

// Função para selecionar categorias dinamicamente baseado nos dados
const selecionarCategoriasDinamicas = (dataA, dataB, maxCategorias = 6) => {
    // Combinar todos os dados e ordenar por maior valor total
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
    
    // Retornar as top categorias ordenadas por valor
    return Array.from(todasCategorias.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, maxCategorias)
        .map(([categoria, _]) => categoria);
};

// Função para calcular métricas interessantes da comparação
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
        
        // Encontrar maior diferença absoluta
        const diferenca = Math.abs(valorA - valorB);
        if (diferenca > maiorDiferenca.valor) {
            maiorDiferenca = {
                categoria: item.categoria,
                valor: diferenca,
                favorito: valorA > valorB ? ufA : ufB
            };
        }
        
        // Encontrar categoria onde cada estado mais investe
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

export default function GraficoComparacao({ ufA, ufB, ano = 2024, onInsightGenerated }) {
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [insight, setInsight] = useState('');
    const [loadingInsight, setLoadingInsight] = useState(false);
    
    // Novos estados para métricas interessantes
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

                // Selecionar categorias dinamicamente baseado nos dados
                const categoriasDinamicas = selecionarCategoriasDinamicas(dataA, dataB, 8);
                
                const mergedDataMap = {};

                // Usar categorias dinâmicas em vez de fixas
                categoriasDinamicas.forEach(cat => {
                    mergedDataMap[cat] = { categoria: cat, [ufA]: 0, [ufB]: 0 };
                });

                dataA.forEach(item => {
                    if (categoriasDinamicas.includes(item.categoria_padronizada)) {
                        mergedDataMap[item.categoria_padronizada][ufA] = item.total_gasto;
                    }
                });

                dataB.forEach(item => {
                    if (categoriasDinamicas.includes(item.categoria_padronizada)) {
                        mergedDataMap[item.categoria_padronizada][ufB] = item.total_gasto;
                    }
                });

                const finalData = Object.values(mergedDataMap).sort((a, b) => {
                    const totalA = (a[ufA] || 0) + (a[ufB] || 0);
                    const totalB = (b[ufA] || 0) + (b[ufB] || 0);
                    return totalB - totalA;
                });

                // Calcular métricas interessantes
                const novasMetricas = calcularMetricas(finalData, ufA, ufB);
                setMetricas(novasMetricas);

                setChartData(finalData);
                
                // Gerar insight automaticamente após carregar os dados
                if (finalData.length > 0) {
                    await gerarInsightIA(finalData, ufA, ufB);
                }

            } catch (error) {
                console.error("Erro ao buscar dados para o gráfico de comparação:", error);
                setChartData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDataForComparison();
    }, [ufA, ufB, ano]);

    const nomeEstadoA = buscarEstado(ufA)?.nome || ufA;
    const nomeEstadoB = buscarEstado(ufB)?.nome || ufB;

    const gerarInsightIA = async (dadosGrafico, estadoA, estadoB) => {
    try {
        setLoadingInsight(true);
        
        // Se não houver API key, usar versão local
        if (!process.env.REACT_APP_OPENAI_API_KEY || process.env.REACT_APP_OPENAI_API_KEY === 'sua_api_key_aqui') {
            const insightLocal = gerarInsightLocal(dadosGrafico, estadoA, estadoB);
            setInsight(insightLocal);
            if (onInsightGenerated) {
                onInsightGenerated(insightLocal, false);
            }
            return;
        }
        
        // Notificar que está carregando
        if (onInsightGenerated) {
            onInsightGenerated('', true); // true = está carregando
        }
        
        // Preparar dados para a IA
            const dadosFormatados = dadosGrafico.map(item => ({
                categoria: item.categoria,
                [estadoA]: formatarValorCompleto(item[estadoA]),
                [estadoB]: formatarValorCompleto(item[estadoB]),
                diferenca: item[estadoA] - item[estadoB],
                diferencaPercentual: item[estadoB] > 0 ? ((item[estadoA] - item[estadoB]) / item[estadoB] * 100).toFixed(1) : 'N/A'
            }));

            const prompt = `
Analise os dados de investimento público entre ${buscarEstado(estadoA)?.nome || estadoA} e ${buscarEstado(estadoB)?.nome || estadoB} nas seguintes categorias:

${dadosFormatados.map(item => 
    `• ${item.categoria}: ${estadoA} ${item[estadoA]} vs ${estadoB} ${item[estadoB]} (diferença: ${item.diferencaPercentual !== 'N/A' ? item.diferencaPercentual + '%' : 'N/A'})`
).join('\n')}

Gere um insight de análise comparativa de no máximo 150 palavras, focando em:
1. Principais diferenças de investimento
2. Áreas onde cada estado se destaca
3. Possíveis implicações ou tendências
4. Conclusão prática

Use linguagem clara e profissional, sem jargões técnicos.`;

            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}` // Você precisará adicionar sua API key aqui
                },
                body: JSON.stringify({
                    model: 'gpt-4.1-nano',
                    messages: [
                        {
                            role: 'system',
                            content: 'Você é um analista especializado em finanças públicas e políticas governamentais. Gere insights claros e práticos sobre investimentos estaduais.'
                        },
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    max_tokens: 300,
                    temperature: 0.7
                })
            });

            if (!response.ok) {
                throw new Error('Erro na API da OpenAI');
            }

            const data = await response.json();
            const insightGerado = data.choices[0]?.message?.content || 'Não foi possível gerar um insight para esta comparação.';
            
            setInsight(insightGerado);
        
        // Notificar o componente pai sobre o insight gerado
        if (onInsightGenerated) {
            onInsightGenerated(insightGerado, false); // false = não está carregando
        }
    } catch (error) {
        console.error('Erro ao gerar insight:', error);
        // Em caso de erro, usar versão local como fallback
        const insightLocal = gerarInsightLocal(dadosGrafico, estadoA, estadoB);
        setInsight(insightLocal);
        if (onInsightGenerated) {
            onInsightGenerated(insightLocal, false);
        }
    } finally {
        setLoadingInsight(false);
    }
    };

    // Função alternativa para gerar insights sem IA (para teste)
    const gerarInsightLocal = (dadosGrafico, estadoA, estadoB) => {
        const nomeA = buscarEstado(estadoA)?.nome || estadoA;
        const nomeB = buscarEstado(estadoB)?.nome || estadoB;
        
        let maiorInvestidorGeral = estadoA;
        let somaA = 0, somaB = 0;
        
        dadosGrafico.forEach(item => {
            somaA += item[estadoA] || 0;
            somaB += item[estadoB] || 0;
        });
        
        if (somaB > somaA) {
            maiorInvestidorGeral = estadoB;
        }
        
        // Encontrar categoria com maior diferença
        let maiorDiferenca = { categoria: '', diferenca: 0, favorito: '' };
        dadosGrafico.forEach(item => {
            const diff = Math.abs((item[estadoA] || 0) - (item[estadoB] || 0));
            if (diff > maiorDiferenca.diferenca) {
                maiorDiferenca = {
                    categoria: item.categoria,
                    diferenca: diff,
                    favorito: (item[estadoA] || 0) > (item[estadoB] || 0) ? estadoA : estadoB
                };
            }
        });
        
        const insight = `Comparando os investimentos entre ${nomeA} e ${nomeB}, observa-se que ${buscarEstado(maiorInvestidorGeral)?.nome || maiorInvestidorGeral} possui maior volume total de investimentos nas categorias analisadas. A maior disparidade ocorre em ${maiorDiferenca.categoria}, onde ${buscarEstado(maiorDiferenca.favorito)?.nome || maiorDiferenca.favorito} investiu significativamente mais. Esta análise sugere diferentes prioridades orçamentárias entre os estados, refletindo suas estratégias de desenvolvimento regional.`;
        
        return insight;
    };

    return (
        <div style={{ width: "100%", height: "100%" }}>
            {/* Cabeçalho com título e métricas */}
            <div style={{ marginBottom: "1rem" }}>
                <h2 style={{ textAlign: "center", color: "#5B228D", marginBottom: "1rem" }}>
                    Comparativo: {nomeEstadoA} vs {nomeEstadoB}
                </h2>
                
                {/* Painel de métricas rápidas */}
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

            <ResponsiveContainer width="100%" height={loading || chartData.length === 0 ? 200 : 350}>
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
