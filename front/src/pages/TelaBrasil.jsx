import React, { useState } from 'react';
import './css/TelaBrasil.css';
//todo - import de svg
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as Moradia } from '../componentes/svg/moradia.svg';
import { ReactComponent as Educacao } from '../componentes/svg/educacao.svg';
import { ReactComponent as Saude } from '../componentes/svg/saude.svg';

//todo - import de funções?
import BtnVerGrafico from '../componentes/botoes/BtnVerGrafico';
import MapaBrasil from '../componentes/mapas/MapaBrasil';
import GraficoTeste from '../componentes/graficos/GraficoTeste';
import RankingNacional from '../componentes/rankings/RankingNacional';

export default function TelaBrasil() {
  const [mostrarGrafico, setMostrarGrafico] = useState(false);

  const dados = [
    {
      id: 1,
      estado: 'São Paulo',
      sigla: 'SP',
      investimento: '2,3 milhões',
      setores: ['Transporte público', 'Tecnologia'],
    },
    {
      id: 2,
      estado: 'Minas Gerais',
      sigla: 'MG',
      investimento: '1,1 milhão',
      setores: ['Educação', 'Agropecuário'],
    },
    {
      id: 3,
      estado: 'Paraná',
      sigla: 'PR',
      investimento: '950 mil',
      setores: ['Alimentício', 'Agropecuário'],
    },
    {
      id: 4,
      estado: 'Rio de Janeiro',
      sigla: 'RJ',
      investimento: '910 mil',
      setores: ['Habitação', 'Turismo'],
    },
    {
      id: 5,
      estado: 'Santa Catarina',
      sigla: 'SC',
      investimento: '860 mil',
      setores: ['Tecnologia'],
    },
  ];

  const compararInvestimento = (a, b) => {
    const parse = (valor) =>
      parseFloat(valor.replace(/[^\d,]/g, '').replace(',', '.'));
    return parse(b.investimento) - parse(a.investimento);
  };

  const [topAreas, setTopAreas] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchTopAreasBrasil = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/analise');
        const data = await response.json();

        // --- ADICIONE ESTA LINHA ---
        console.log('Dados recebidos no React:', data);
        // --------------------------

        if (data && data.length >= 2) {
          setTopAreas(data);
        }
      } catch (error) {
        console.error('Erro ao buscar dados da análise:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTopAreasBrasil();
  }, []);
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
                {loading || topAreas.length < 1
                  ? '#'
                  : topAreas[0].categoria_padronizada}
              </strong>{' '}
              e{' '}
              <strong style={{ color: '#0EC0D1' }}>
                {loading || topAreas.length < 2
                  ? '#'
                  : topAreas[1].categoria_padronizada}
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
              <RankingNacional items={dados} compareFn={compararInvestimento} />
            )}
          </div>
        </div>
      </div>

      <div className="container-cards">
        <div className="card">
          <Moradia width="80px" height="80px" />
          <p>
            O <strong>estado X</strong> gasta <strong>2x</strong> mais em
            habitação que a média nacional
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
    </div> // todo fim do return
  );
}
