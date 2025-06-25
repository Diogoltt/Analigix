import React, { useState, useEffect, useRef } from "react";
import "./css/TelaBrasil.css";
import { ESTADOS_BR } from '../util/Estados';

import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as Moradia } from '../componentes/svg/moradia.svg';
import { ReactComponent as Educacao } from '../componentes/svg/educacao.svg';
import { ReactComponent as Saude } from '../componentes/svg/saude.svg';

import BtnVerGrafico from "../componentes/botoes/BtnVerGrafico";
import BtnBuscaEstado from "../componentes/botoes/BtnBuscaEstado";
import BtnComparar from "../componentes/botoes/BtnComparar";

import MapaBrasil from "../componentes/mapas/MapaBrasil";
import GraficoBarras from "../componentes/graficos/GraficoBarras";
import GraficoComparacao from "../componentes/graficos/GraficoComparacao";

import RankingNacional from "../componentes/rankings/RankingNacional";

export default function TelaBrasil() {
  //=========== BUSCA PRINCIPAL ===========
  const [buscaEstado, setBuscaEstado] = useState("");
  const [mostrarSugestoes, setMostrarSugestoes] = useState(false);
  const [estadosFiltrados, setEstadosFiltrados] = useState([]);
  const inputRef = useRef(null);

  useEffect(() => {
    setEstadosFiltrados(filterEstados(buscaEstado));
  }, [buscaEstado]);

  const handleSelectEstado = (nome) => {
    setBuscaEstado(nome);
    setMostrarSugestoes(false);
    inputRef.current.focus();
  };

  //=========== RANKING ===========
  const [mostrarGrafico, setMostrarGrafico] = useState(false);
  const dados = [
    { id: 1, estado: "São Paulo", sigla: "SP", investimento: "2,3 milhões", setores: ["Transporte público", "Tecnologia"] },
    { id: 2, estado: "Minas Gerais", sigla: "MG", investimento: "1,1 milhão", setores: ["Educação", "Agropecuário"] },
    { id: 3, estado: "Paraná", sigla: "PR", investimento: "950 mil", setores: ["Alimentício", "Agropecuário"] },
    { id: 4, estado: "Rio de Janeiro", sigla: "RJ", investimento: "910 mil", setores: ["Habitação", "Turismo"] },
    { id: 5, estado: "Santa Catarina", sigla: "SC", investimento: "860 mil", setores: ["Tecnologia"] },
  ];

  //=========== COMPARAÇÃO ===========
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


  const filterEstados = (termo) => {
    if (!termo.trim()) return [];

    const termoLower = termo.toLowerCase();
    
    return Object.entries(ESTADOS_BR)
      .filter(([nome, sigla]) => {
        const nomeLower = nome.toLowerCase();
        const siglaLower = sigla.toLowerCase();
        return nomeLower.startsWith(termoLower) ||
          siglaLower === termoLower; // Comparação exata para sigla
      })
      .slice(0, 5);
  };


  useEffect(() => {
    setEstadosFiltradosA(filterEstados(estadoA));
  }, [estadoA]);


  useEffect(() => {
    setEstadosFiltradosB(filterEstados(estadoB));
  }, [estadoB]);


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

  // Handler para comparação
  const handleComparar = (ufA, ufB) => {
    setUfsComparadas([ufA, ufB]);
    setMostrarComparacao(true);
  };

  // Função para comparar investimentos --> contém dados fictios
  const compararInvestimento = (a, b) => {
    const parse = valor => parseFloat(valor.replace(/[^\d,]/g, "").replace(",", "."));
    return parse(b.investimento) - parse(a.investimento);
  };

  return (
    <div>
      <nav className="navbar">
        <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
        <a href="/Portais-da-Transparencia" style={{ color: "white" }}>Portais da Transparência</a>
      </nav>

      {/* Busca de estado */}
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

      {/* Mapa e ranking */}
      <div className="container-mapa-ranking">
        <div className="mapaBrasil">
          <MapaBrasil style={{ maxWidth: "100%", height: "auto" }} />
        </div>

        <div className="info-container">
          <div className="info-nacional">
            <h1 style={{ color: "#5B228D", textAlign: "center", marginBottom: "1.5rem" }}>
              Exemplo: No último ano o País investiu mais em <strong style={{ color: "#0EC0D1" }}>#</strong> e <strong style={{ color: "#0EC0D1" }}>#</strong>
            </h1>
            <BtnVerGrafico mostrarGrafico={mostrarGrafico} setMostrarGrafico={setMostrarGrafico} text={mostrarGrafico ? "Ranking" : "Grafico"} />
          </div>

          <div className="conteudo-ranking-grafico">
            {mostrarGrafico ? (
              <GraficoBarras />
            ) : (
              <RankingNacional items={dados} compareFn={compararInvestimento} />
            )}
          </div>
        </div>
      </div>

      {/* Cards */}
      <div className="container-cards">
        <div className="card">
          <Moradia width="80px" height="80px" />
          <p>
            O <strong>estado X</strong> gasta <strong>2x</strong> mais em habitação que a média nacional
          </p>
        </div>
        <div className="card">
          <Educacao width="80px" height="80px" />
          <p>
            O <strong>estado X </strong> recebeu <strong>X </strong> para a área da educação
          </p>
        </div>
        <div className="card">
          <Saude width="80px" height="80px" />
          <p>
            O <strong>estado X </strong> disponibilizou <strong>X </strong> para a saúde
          </p>
        </div>
      </div>

      {/* Comparação */}
      <div className="container-comparacao">
        <div className="titulo-comparacao">
          <h1 style={{ color: "#5B228D" }}>Comparação entre estados</h1>
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
              <GraficoComparacao ufA={ufsComparadas[0]} ufB={ufsComparadas[1]} />
            </div>
            <div className="insights">
              <h2>Exemplo de insight com base no gráfico de comparação</h2>
              {/* Trazer a análise de dados aqui */}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}