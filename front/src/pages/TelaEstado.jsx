import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './css/TelaEstado.css';
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as AlfineteMapa } from '../componentes/svg/alfinete.svg';
import BtnVoltar from '../componentes/botoes/BtnVoltarTela.jsx';
import RankingEstadual from '../componentes/rankings/RankingEstadual.jsx';
import GraficoPerfil from '../componentes/graficos/GraficoPerfil.jsx';
import GraficoPizza from '../componentes/graficos/GraficoPizza.jsx';


export default function TelaEstado() {
 
  const { uf } = useParams();
  const navigate = useNavigate();
  const handleClick = () => navigate('/nacional');

  const [anoSelecionado, setAnoSelecionado] = useState('');
  const [rankingData, setRankingData] = useState([]);
  const [valorTotal, setValorTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const [rankingPage, setRankingPage] = useState(1);
  const [totalRankingItems, setTotalRankingItems] = useState(0);
  const recordsPerPage = 10;

 
  useEffect(() => {
    setRankingPage(1);
  }, [anoSelecionado]);

  useEffect(() => {
    const fetchDataForState = async () => {
      if (!uf) return;
      setLoading(true);

      const params = new URLSearchParams();
      params.append('uf', uf);
      if (anoSelecionado) params.append('ano', anoSelecionado);

      const rankingParams = new URLSearchParams(params);
      rankingParams.append('page', rankingPage);
      rankingParams.append('per_page', recordsPerPage);

      const rankingApiUrl = `http://127.0.0.1:5000/api/ranking?${rankingParams.toString()}`;
      const totalApiUrl = `http://127.0.0.1:5000/api/estatisticas/total?${params.toString()}`;

      try {
        const [rankingResponse, totalResponse] = await Promise.all([
          fetch(rankingApiUrl),
          fetch(totalApiUrl),
        ]);

        const rankingResult = await rankingResponse.json();
        const totalResult = await totalResponse.json();

        setRankingData(rankingResult.dados || []);
        setTotalRankingItems(rankingResult.total_registros || 0);
        setValorTotal(totalResult.valor_total || 0);
      } catch (error) {
        console.error('Erro ao buscar dados do estado:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDataForState();
  }, [uf, anoSelecionado, rankingPage]);

  const totalPages = Math.ceil(totalRankingItems / recordsPerPage);

  
  return (
    <div>
      <nav className="navbar">
        <a href="/nacional">
          <LogoAnaligixAzul width="200px" height="80px" />
        </a>
        <a
          href="/Portais-da-Transparencia"
          style={{ color: 'white', font: '' }}
        >
          Portais da Transparência
        </a>
      </nav>
      <div className="container-Principal">
        <div className="container-1">
          <div className="btnVoltar">
            <BtnVoltar texto="Voltar" onClick={handleClick} />
          </div>
          <div className="nome-Estado-Filtro">
            <h1
              style={{
                color: '#2C006A',
                display: 'flex',
                alignItems: 'center',
                flexWrap: 'wrap',
              }}
            >
              <AlfineteMapa />
              <span style={{ marginLeft: '10px' }}>{uf}</span>
              <span
                style={{
                  marginLeft: '20px',
                  fontSize: '1.2rem',
                  color: '#555',
                }}
              >
                - Total Investido ({anoSelecionado || 'Todos os anos'}):
                {loading
                  ? '...'
                  : ` R$ ${valorTotal.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}`}
              </span>
            </h1>
            <select
              className="filtro"
              name="ano"
              id="ano"
              value={anoSelecionado}
              onChange={(e) => setAnoSelecionado(e.target.value)}
            >
              <option value="">Todos os anos</option>
              <option value="2024">2024</option>
              <option value="2023">2023</option>
              <option value="2022">2022</option>
              <option value="2021">2021</option>
              <option value="2020">2020</option>
            </select>
          </div>

          <div className="ranking-Estadual">
            {loading ? (
              <p>Carregando ranking...</p>
            ) : (
              <RankingEstadual
                items={rankingData}
                page={rankingPage}
                perPage={recordsPerPage}
                uf={uf}
                ano={anoSelecionado}
              />
            )}

            <div
              className="pagination-ranking"
              style={{ textAlign: 'center', marginTop: '1rem' }}
            >
              <button
                className="btn-ranking"
                onClick={() => setRankingPage(rankingPage - 1)}
                disabled={rankingPage <= 1 || loading}
              >
                Anterior
              </button>
              <span style={{ margin: '0 1rem' }}>
                Página {rankingPage} de {totalPages || 1}
              </span>
              <button
                className="btn-ranking"
                onClick={() => setRankingPage(rankingPage + 1)}
                disabled={rankingPage >= totalPages || loading}
              >
                Próximo
              </button>
            </div>
          </div>
        </div>
        <div className="container-2">
          <div className="mapa-Estado">
            <GraficoPizza uf={uf} anoSelecionado={anoSelecionado} />
          </div>
          <div className="grafico-Estado">
            <GraficoPerfil chartData={rankingData} />
          </div>
        </div>
      </div>
    </div>
  );
}
