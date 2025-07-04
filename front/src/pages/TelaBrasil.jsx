import React, { useState, useEffect, useRef, useCallback } from 'react';
import './css/TelaBrasil.css';

import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as Moradia } from '../componentes/svg/moradia.svg';
import { ReactComponent as Educacao } from '../componentes/svg/educacao.svg';
import { ReactComponent as Saude } from '../componentes/svg/saude.svg';
import { ESTADOS_BR } from '../util/Estados';

import BtnVerGrafico from '../componentes/botoes/BtnVerGrafico';
import BtnBuscaEstado from '../componentes/botoes/BtnBuscaEstado';
import BtnComparar from '../componentes/botoes/BtnComparar';
import MapaBrasil from '../componentes/mapas/MapaBrasil';
import GraficoBarras from '../componentes/graficos/GraficoBarras';
import GraficoComparacao from '../componentes/graficos/GraficoComparacao';
import RankingNacional from '../componentes/rankings/RankingNacional';
import TypewriterText from '../componentes/efeitos/TypewriterText';
import '../componentes/efeitos/TypewriterText.css';

export default function TelaBrasil() {
    const [anoSelecionado, setAnoSelecionado] = useState(2024); // Ano padrão
    const [topAreasNacional, setTopAreasNacional] = useState([]);
    const [rankingNacionalData, setRankingNacionalData] = useState([]);
    const [topStateInfo, setTopStateInfo] = useState({ uf: '...', categoria: '...' });
    const [loading, setLoading] = useState(true);

    const [buscaEstado, setBuscaEstado] = useState("");
    const [mostrarSugestoes, setMostrarSugestoes] = useState(false);
    const [estadosFiltrados, setEstadosFiltrados] = useState([]);
    const inputRef = useRef(null);

    const [mostrarGrafico, setMostrarGrafico] = useState(false);

    const [estadoA, setEstadoA] = useState("");
    const [estadoB, setEstadoB] = useState("");
    const [mostrarSugestoesA, setMostrarSugestoesA] = useState(false);
    const [mostrarSugestoesB, setMostrarSugestoesB] = useState(false);
    const [estadosFiltradosA, setEstadosFiltradosA] = useState([]);
    const [estadosFiltradosB, setEstadosFiltradosB] = useState([]);
    const inputRefA = useRef(null);
    const inputRefB = useRef(null);
    const [mostrarComparacao, setMostrarComparacao] = useState(false);
    const [ufsComparadas, setUfsComparadas] = useState([]);
    const [insightTexto, setInsightTexto] = useState('');
    const [insightCarregando, setInsightCarregando] = useState(false);
    const [mostrarTypewriter, setMostrarTypewriter] = useState(false);
    const [categoriasSelecionadas, setCategoriasSelecionadas] = useState([]);

    useEffect(() => {
        const fetchInitialData = async () => {
            setLoading(true); // Garantir que loading seja true ao iniciar nova busca
            try {
                const [analiseResponse, rankingResponse] = await Promise.all([
                    fetch(`http://127.0.0.1:5000/api/analise?ano=${anoSelecionado}`),
                    fetch(`http://127.0.0.1:5000/api/ranking-nacional?ano=${anoSelecionado}`)
                ]);

                const analiseData = await analiseResponse.json();
                const rankingData = await rankingResponse.json();

                // Reset dos dados para evitar exibição de dados antigos quando não há dados para o ano
                if (analiseData && analiseData.length >= 2) {
                    setTopAreasNacional(analiseData);
                } else {
                    setTopAreasNacional([]); // Limpa dados anteriores
                }
                
                if (rankingData && rankingData.length > 0) {
                    setRankingNacionalData(rankingData);
                } else {
                    setRankingNacionalData([]); // Limpa dados anteriores
                }
            } catch (error) {
                console.error('Erro ao buscar dados iniciais:', error);
                // Em caso de erro, também limpa os dados
                setTopAreasNacional([]);
                setRankingNacionalData([]);
            } finally {
                setLoading(false);
            }
        };
        fetchInitialData();
    }, [anoSelecionado]);

    useEffect(() => {
        if (rankingNacionalData.length > 0) {
            const topStateUf = rankingNacionalData[0].estado;
            const fetchTopStateCategory = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/analise?uf=${topStateUf}&ano=${anoSelecionado}`);
                    const data = await response.json();
                    if (data && data.length > 0) {
                        setTopStateInfo({
                            uf: topStateUf,
                            categoria: data[0].categoria_padronizada
                        });
                    } else {
                        setTopStateInfo({ uf: '...', categoria: '...' });
                    }
                } catch (error) {
                    console.error(`Erro ao buscar detalhes para ${topStateUf}:`, error);
                    setTopStateInfo({ uf: '...', categoria: '...' });
                }
            };
            fetchTopStateCategory();
        } else {
            // Reset quando não há dados de ranking
            setTopStateInfo({ uf: '...', categoria: '...' });
        }
    }, [rankingNacionalData, anoSelecionado]);

    const filterEstados = (termo) => {
        if (!termo.trim()) return [];
        const termoLower = termo.toLowerCase();
        return Object.entries(ESTADOS_BR)
            .filter(([nome, sigla]) => {
                const nomeLower = nome.toLowerCase();
                const siglaLower = sigla.toLowerCase();
                return nomeLower.startsWith(termoLower) || siglaLower === termoLower;
            })
            .slice(0, 5);
    };

    useEffect(() => {
        setEstadosFiltrados(filterEstados(buscaEstado));
    }, [buscaEstado]);

    useEffect(() => {
        setEstadosFiltradosA(filterEstados(estadoA));
    }, [estadoA]);

    useEffect(() => {
        setEstadosFiltradosB(filterEstados(estadoB));
    }, [estadoB]);

    const handleSelectEstado = (nome) => {
        setBuscaEstado(nome);
        setMostrarSugestoes(false);
        inputRef.current.focus();
    };

    const handleSelectEstadoA = (nome) => {
        setEstadoA(nome);
        setMostrarSugestoesA(false);
        inputRefA.current.focus();
    };

    const handleSelectEstadoB = (nome) => {
        setEstadoB(nome);
        setMostrarSugestoesB(false);
        inputRefB.current.focus();
    };

    const handleComparar = (ufA, ufB) => {
        setMostrarComparacao(true);
        
        setInsightTexto('');
        setMostrarTypewriter(false);
        setInsightCarregando(false);
    };

    const handleInsightGenerated = (insightText, isLoading) => {
        setInsightCarregando(isLoading);
        if (!isLoading && insightText) {
            setInsightTexto(insightText);
            setMostrarTypewriter(true);
        }
    };

    const gerarInsight = async () => {
        if (!mostrarComparacao) return;

        setInsightCarregando(true);
        setInsightTexto('');
        setMostrarTypewriter(false);

        try {
            
            let url = `http://127.0.0.1:5000/api/insight-comparacao?ufA=${ESTADOS_BR[estadoA]}&ufB=${ESTADOS_BR[estadoB]}&ano=${anoSelecionado}`;

            if (categoriasSelecionadas.length > 0) {
                url += `&categorias=${categoriasSelecionadas.join(',')}`;
            }

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error('Erro ao gerar insight');
            }

            const data = await response.json();

            if (data.insight) {
                handleInsightGenerated(data.insight, false);
            } else {
                const insight = `Comparação entre ${estadoA} e ${estadoB}: Análise dos dados de ${anoSelecionado} mostra padrões distintos de investimento público. Os estados apresentam diferentes estratégias de alocação de recursos, refletindo suas prioridades regionais e necessidades específicas.`;
                handleInsightGenerated(insight, false);
            }
            
        } catch (error) {
            console.error('Erro ao gerar insight:', error);
            const insight = `Comparação entre ${estadoA} e ${estadoB}: Não foi possível acessar dados detalhados no momento. Recomenda-se verificar a conectividade e tentar novamente para uma análise mais precisa dos padrões de investimento.`;
            handleInsightGenerated(insight, false);
        }
    };

    const handleCategoriasChange = useCallback((novasCategorias) => {
        setCategoriasSelecionadas(novasCategorias);
    }, []);

    return (
        <div>
            <nav className="navbar">
                <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
                <div className="nav-links">
                    <a href="/tendencias" style={{ color: "white" }}>Tendências</a>
                    <a href="/portais-da-Transparencia" style={{ color: "white" }}>Portais da Transparência</a>
                </div>
            </nav>
            <div className="BuscaEstado">
                <input
                    ref={inputRef}
                    className="busca-input"
                    type="text"
                    placeholder="🔍︎ Digite o estado ou sigla"
                    value={buscaEstado}
                    onChange={(e) => {
                        setBuscaEstado(e.target.value);
                        setMostrarSugestoes(true);
                    }}
                    onFocus={() => setMostrarSugestoes(true)}
                    onBlur={() => setTimeout(() => setMostrarSugestoes(false), 200)}
                />
                {mostrarSugestoes && estadosFiltrados.length > 0 && (
                    <div className="sugestoes-container">
                        {estadosFiltrados.map(([nome, sigla]) => (
                            <div
                                key={`busca-${sigla}`}
                                className="sugestao-item"
                                onClick={() => handleSelectEstado(nome)}
                                onMouseDown={(e) => e.preventDefault()}
                            >
                                {nome} ({sigla})
                            </div>
                        ))}
                    </div>
                )}
                <BtnBuscaEstado estado={buscaEstado} />
            </div>
            <div className="container-mapa-ranking">
                <div className="filtro-ano">
                    <label htmlFor="seletor-ano" style={{ color: '#2C006A', marginRight: '1px' }}>Ano de análise:</label>
                    <select
                        className='seletor-ano'
                        id="seletor-ano"
                        value={anoSelecionado}
                        onChange={(e) => setAnoSelecionado(parseInt(e.target.value))}
                        style={{
                            backgroundColor: '#fff',
                            border: '1px solid #ccc',
                            borderRadius: '8px',
                            padding: '10px 16px',
                            fontSize: '16px',
                            maxWidth: '90%',
                            color: '#333',
                            boxShadow: '0 1px 4px rgba(0,0,0,0.05)',
                            transition: 'all 0.2s ease-in-out'
                        }}
                    >
                        <option value={2024}>2024</option>
                        <option value={2023}>2023</option>
                        <option value={2022}>2022</option>
                        <option value={2021}>2021</option>
                        <option value={2020}>2020</option>
                    </select>
                </div>
                <div className='mapa-ranking'>
                    <div className="mapaBrasil">
                        <MapaBrasil style={{ maxWidth: '100%', height: 'auto' }} />
                    </div>
                    <div className="info-container">
                        <div className="info-nacional">
                            {loading ? (
                                <h1 style={{ color: '#2C006A', textAlign: 'center', marginBottom: '1.5rem' }}>
                                    Carregando dados para <strong style={{ color: '#0EC0D1' }}>{anoSelecionado}</strong>...
                                </h1>
                            ) : topAreasNacional.length >= 2 ? (
                                <h1 style={{ color: '#2C006A', textAlign: 'center', marginBottom: '1.5rem' }}>
                                    No ano <strong style={{ color: '#0EC0D1' }}>{anoSelecionado}</strong> o País investiu mais em{' '}
                                    <strong style={{ color: '#0EC0D1' }}>
                                        {topAreasNacional[0].categoria_padronizada}
                                    </strong>{' '}
                                    e{' '}
                                    <strong style={{ color: '#0EC0D1' }}>
                                        {topAreasNacional[1].categoria_padronizada}
                                    </strong>
                                </h1>
                            ) : (
                                <h1 style={{ color: '#2C006A', textAlign: 'center', marginBottom: '1.5rem' }}>
                                    Não há dados disponíveis para o ano <strong style={{ color: '#FF5A1F' }}>{anoSelecionado}</strong>
                                </h1>
                            )}
                            <BtnVerGrafico
                                mostrarGrafico={mostrarGrafico}
                                setMostrarGrafico={setMostrarGrafico}
                                text={mostrarGrafico ? 'Ranking' : 'Grafico'}
                                disabled={!loading && topAreasNacional.length === 0 && rankingNacionalData.length === 0}
                            />
                        </div>

                        <div className="conteudo-ranking-grafico">
                            {!loading && topAreasNacional.length === 0 && rankingNacionalData.length === 0 ? (
                                <div className="empty-data-container">
                                    <div className="empty-data-icon">📊</div>
                                    <div className="empty-data-message">Sem dados disponíveis para {anoSelecionado}</div>
                                    <div className="empty-data-submessage">Selecione um ano diferente ou verifique se há dados no sistema</div>
                                </div>
                            ) : mostrarGrafico ? (
                                <GraficoBarras ano={anoSelecionado} />
                            ) : (
                                <RankingNacional items={rankingNacionalData} />
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="container-comparacao">
                <div className="titulo-comparacao">
                    <h1 style={{ color: "#2C006A" }}>Comparação entre estados</h1>
                </div>
                <div>
                    <form className="forms-Grafico" onSubmit={(e) => e.preventDefault()}>
                        <div className="input-container">
                            <label className="campo-Grafico">Selecione o Estado A: </label>
                            <input
                                ref={inputRefA}
                                className="busca-input"
                                type="text"
                                value={estadoA}
                                onChange={(e) => {
                                    setEstadoA(e.target.value);
                                    setMostrarSugestoesA(true);
                                }}
                                onFocus={() => setMostrarSugestoesA(true)}
                                onBlur={() => setTimeout(() => setMostrarSugestoesA(false), 200)}
                                placeholder="Digite o estado ou sigla"
                            />
                            {mostrarSugestoesA && estadosFiltradosA.length > 0 && (
                                <div className="sugestoes-containerA">
                                    {estadosFiltradosA.map(([nome, sigla]) => (
                                        <div
                                            key={`A-${sigla}`}
                                            className="sugestao-item"
                                            onClick={() => handleSelectEstadoA(nome)}
                                            onMouseDown={(e) => e.preventDefault()}
                                        >
                                            {nome} ({sigla})
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div className="input-container">
                            <label className="campo-Grafico">Selecione o Estado B: </label>
                            <input
                                ref={inputRefB}
                                className="busca-input"
                                type="text"
                                value={estadoB}
                                onChange={(e) => {
                                    setEstadoB(e.target.value);
                                    setMostrarSugestoesB(true);
                                }}
                                onFocus={() => setMostrarSugestoesB(true)}
                                onBlur={() => setTimeout(() => setMostrarSugestoesB(false), 200)}
                                placeholder="Digite o estado ou sigla"
                            />
                            {mostrarSugestoesB && estadosFiltradosB.length > 0 && (
                                <div className="sugestoes-containerA">
                                    {estadosFiltradosB.map(([nome, sigla]) => (
                                        <div
                                            key={`B-${sigla}`}
                                            className="sugestao-item"
                                            onClick={() => handleSelectEstadoB(nome)}
                                            onMouseDown={(e) => e.preventDefault()}
                                        >
                                            {nome} ({sigla})
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                        <BtnComparar estadoA={estadoA} estadoB={estadoB} onComparar={handleComparar} />
                    </form>
                </div>
                {mostrarComparacao && (
                    <div className="grafico-insights">
                        <div className="grafico-Comparacao">
                            <GraficoComparacao
                                ufA={ESTADOS_BR[estadoA]}
                                ufB={ESTADOS_BR[estadoB]}
                                ano={anoSelecionado}
                                onInsightGenerated={handleInsightGenerated}
                                onCategoriasChange={handleCategoriasChange}
                            />
                        </div>
                        <div className="insights">
                            <h2>
                                💡 Insights da Comparação
                                <span className="insights-badge">Gerado por IA</span>
                            </h2>

                            {insightCarregando ? (
                                <div className="insights-loading">
                                    <div className="loading-spinner"></div>
                                    Analisando dados e gerando insights...
                                </div>
                            ) : insightTexto ? (
                                <div>
                                    <p className="insights-content">
                                        {mostrarTypewriter ? (
                                            <TypewriterText
                                                text={insightTexto}
                                                speed={30}
                                                onComplete={() => console.log('Typewriter finalizado')}
                                            />
                                        ) : (
                                            insightTexto
                                        )}
                                    </p>
                                    <button
                                        onClick={gerarInsight}
                                        className="btn-gerar-insight"
                                        style={{
                                            marginTop: '15px',
                                            padding: '8px 16px',
                                            backgroundColor: '#5B228D',
                                            color: '#fff',
                                            border: 'none',
                                            borderRadius: '6px',
                                            cursor: 'pointer',
                                            fontSize: '0.9rem',
                                            fontWeight: 'bold'
                                        }}
                                    >
                                        🔄 Gerar Novo Insight
                                    </button>
                                </div>
                            ) : (
                                <div>
                                    <p className="insights-content">
                                        Clique no botão abaixo para gerar uma análise comparativa baseada nas categorias atualmente selecionadas no gráfico.
                                    </p>
                                    <button
                                        onClick={gerarInsight}
                                        className="btn-gerar-insight"
                                        style={{
                                            marginTop: '15px',
                                            padding: '8px 16px',
                                            backgroundColor: '#5B228D',
                                            color: '#fff',
                                            border: 'none',
                                            borderRadius: '6px',
                                            cursor: 'pointer',
                                            fontSize: '0.9rem',
                                            fontWeight: 'bold'
                                        }}
                                    >
                                        🧠 Gerar Insight
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}