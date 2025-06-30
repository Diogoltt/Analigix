import React, { useState, useEffect, useRef } from 'react';
import './css/TelaBrasil.css';

// Imports de SVGs e Utilitários de ambas as versões
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as Moradia } from '../componentes/svg/moradia.svg';
import { ReactComponent as Educacao } from '../componentes/svg/educacao.svg';
import { ReactComponent as Saude } from '../componentes/svg/saude.svg';
import { ESTADOS_BR } from '../util/Estados';

// Imports de Componentes de ambas as versões
import BtnVerGrafico from '../componentes/botoes/BtnVerGrafico';
import BtnBuscaEstado from '../componentes/botoes/BtnBuscaEstado';
import BtnComparar from '../componentes/botoes/BtnComparar';
import MapaBrasil from '../componentes/mapas/MapaBrasil';
import GraficoBarras from '../componentes/graficos/GraficoBarras';
import GraficoComparacao from '../componentes/graficos/GraficoComparacao';
import RankingNacional from '../componentes/rankings/RankingNacional';

export default function TelaBrasil() {
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

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [analiseResponse, rankingResponse] = await Promise.all([
                    fetch('http://127.0.0.1:5000/api/analise'), 
                    fetch('http://127.0.0.1:5000/api/ranking-nacional')
                ]);

                const analiseData = await analiseResponse.json();
                const rankingData = await rankingResponse.json();

                if (analiseData && analiseData.length >= 2) {
                    setTopAreasNacional(analiseData);
                }
                if (rankingData && rankingData.length > 0) {
                    setRankingNacionalData(rankingData);
                }
            } catch (error) {
                console.error('Erro ao buscar dados iniciais:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchInitialData();
    }, []);

    useEffect(() => {
        if (rankingNacionalData.length > 0) {
            const topStateUf = rankingNacionalData[0].estado;
            const fetchTopStateCategory = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/analise?uf=${topStateUf}`);
                    const data = await response.json();
                    if (data && data.length > 0) {
                        setTopStateInfo({
                            uf: topStateUf,
                            categoria: data[0].categoria_padronizada
                        });
                    }
                } catch (error) {
                    console.error(`Erro ao buscar detalhes para ${topStateUf}:`, error);
                }
            };
            fetchTopStateCategory();
        }
    }, [rankingNacionalData]);

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
        setUfsComparadas([ufA, ufB]);
        setMostrarComparacao(true);
    };


    return (
        <div>
            <nav className="navbar">
                <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
               <a href="/Portais-da-Transparencia" style={{ color: "white", font: "" }}>Portais da Transparência</a>

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
                <div className="mapaBrasil">
                    <MapaBrasil style={{ maxWidth: '100%', height: 'auto' }} />
                </div>

                <div className="info-container">
                    <div className="info-nacional">
                        <h1 style={{ color: '#2C006A', textAlign: 'center', marginBottom: '1.5rem' }}>
                            No último ano o País investiu mais em{' '}
                            <strong style={{ color: '#0EC0D1' }}>
                                {loading || topAreasNacional.length < 1 ? '...' : topAreasNacional[0].categoria_padronizada}
                            </strong>{' '}
                            e{' '}
                            <strong style={{ color: '#0EC0D1' }}>
                                {loading || topAreasNacional.length < 2 ? '...' : topAreasNacional[1].categoria_padronizada}
                            </strong>
                        </h1>
                        <BtnVerGrafico
                            mostrarGrafico={mostrarGrafico}
                            setMostrarGrafico={setMostrarGrafico}
                            text={mostrarGrafico ? 'Ranking' : 'Grafico'}
                        />
                    </div>

                    <div className="conteudo-ranking-grafico">
                        {mostrarGrafico ? (
                            <GraficoBarras />
                        ) : (
                            <RankingNacional items={rankingNacionalData} />
                        )}
                    </div>
                </div>
            </div>
            <div className="container-cards">
                <div className="card">
                    <Moradia width="80px" height="80px" />
                    <p>
                        O estado campeão de investimentos, <strong>{loading ? '...' : topStateInfo.uf}</strong>,
                        destaca-se pelos gastos na área de <strong>{loading ? '...' : topStateInfo.categoria}</strong>.
                    </p>
                </div>             
                <div className="card">
                    <Educacao width="80px" height="80px" />
                    <p>
                        O <strong>estado X </strong> recebeu <strong>X </strong> para a área
                        da educação
                    </p>
                </div>
                <div className="card">
                    <Saude width="80px" height="80px" />
                    <p>
                        O <strong>estado X </strong> disponibilizou <strong>X </strong> para
                        a saúde
                    </p>
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
                                placeholder="Digite ou selecione um estado"
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
                                placeholder="Digite ou selecione um estado"
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
                            <GraficoComparacao ufA={ESTADOS_BR[estadoA]} ufB={ESTADOS_BR[estadoB]} />
                        </div>
                        <div className="insights">
                            <h2>Exemplo de insight com base no gráfico de comparação</h2>
                        </div>
                    </div>
                )}
            </div>   
        </div>
    );
}