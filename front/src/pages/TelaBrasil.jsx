import React, { useState, useEffect } from 'react';
import './css/TelaBrasil.css';

// Seus imports de SVGs e Componentes
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as Moradia } from '../componentes/svg/moradia.svg';
import { ReactComponent as Educacao } from '../componentes/svg/educacao.svg';
import { ReactComponent as Saude } from '../componentes/svg/saude.svg';
import BtnVerGrafico from '../componentes/botoes/BtnVerGrafico';
import MapaBrasil from '../componentes/mapas/MapaBrasil';
import GraficoTeste from '../componentes/graficos/GraficoTeste';
import RankingNacional from '../componentes/rankings/RankingNacional';

export default function TelaBrasil() {
    const [mostrarGrafico, setMostrarGrafico] = useState(false);
    
    // Estados para guardar os dados vindos da API
    const [topAreasNacional, setTopAreasNacional] = useState([]);
    const [rankingNacionalData, setRankingNacionalData] = useState([]);
    const [topStateInfo, setTopStateInfo] = useState({ uf: '...', categoria: '...' });
    const [loading, setLoading] = useState(true);

    // EFEITO 1: Busca os dados gerais da página (Top 2 Nacional e Ranking de Estados)
    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                // Usamos Promise.all para fazer as duas buscas ao mesmo tempo
                const [analiseResponse, rankingResponse] = await Promise.all([
                    fetch('http://127.0.0.1:5000/api/analise'), // Top 2 do Brasil
                    fetch('http://127.0.0.1:5000/api/ranking-nacional') // Top 5 estados
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
                // Apenas paramos o loading geral aqui
                setLoading(false);
            }
        };

        fetchInitialData();
    }, []); // O array vazio [] garante que esta busca ocorra apenas uma vez

    // EFEITO 2: Busca os detalhes do estado Top 1 (roda DEPOIS que a primeira busca termina)
    useEffect(() => {
        if (rankingNacionalData.length > 0) {
            const topStateUf = rankingNacionalData[0].estado; // Pega a sigla do 1º do ranking

            const fetchTopStateCategory = async () => {
                try {
                    // Faz a segunda busca, para os detalhes daquele estado específico
                    const response = await fetch(`http://127.0.0.1:5000/api/analise?uf=${topStateUf}`);
                    const data = await response.json();
                    
                    if (data && data.length > 0) {
                        // Guarda a sigla do estado e sua principal categoria de investimento
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
    }, [rankingNacionalData]); // A dependência faz este efeito rodar sempre que o ranking for atualizado

    return (
        <div>
            <nav className="navbar">
                <a href="/analigix">
                    <LogoAnaligixAzul width="200px" height="80px" />
                </a>
            </nav>

            <div className="container-mapa-ranking">
                <div className="mapaBrasil">
                    <MapaBrasil style={{ maxWidth: '100%', height: 'auto' }} />
                </div>

                <div className="info-container">
                    <div className="info-nacional">
                        <h1
                            style={{
                                color: '#2C006A',
                                textAlign: 'center',
                                marginBottom: '1.5rem',
                            }}
                        >
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
                            <GraficoTeste />
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
                        O estado campeão de investimentos, <strong>{topStateInfo.uf}</strong>, 
                        destaca-se pelos gastos na área de <strong>{topStateInfo.categoria}</strong>.
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

            <div className="container-novos-Produtos">
                <div className="novos-Produtos-titulo">
                    <h1 style={{ color: '#2C006A' }}>
                        Sugestão de áreas para Novos Produtos
                    </h1>
                </div>
                <div className="novos-produtos-info">
                    <h2>Lero lero titulo de possível investimento</h2>
                    <p>
                        Lero lero trazer a análise de dados aqui para previsões futuras{' '}
                        <br />
                        lero lero numeros <br />
                        lero lero mais numeros <br />
                        lero lero estado <br />
                    </p>
                </div>
            </div>
        </div>
    );
}