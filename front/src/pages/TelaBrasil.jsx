import React, { useState } from "react";
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
import GraficoTornado from "../componentes/graficos/GraficoTornado";

import RankingNacional from "../componentes/rankings/RankingNacional";

export default function TelaBrasil() {
  const [mostrarGrafico, setMostrarGrafico] = useState(false);
  const [buscaEstado, setBuscaEstado] = useState("");

  const [estadoA, setEstadoA] = useState("");
  const [estadoB, setEstadoB] = useState("");
  const [ufsComparadas, setUfsComparadas] = useState(null); // ex: ["SP", "RJ"]

  const handleBuscaChange = (e) => {
    setBuscaEstado(e.target.value);
  };

  const dados = [
    { id: 1, estado: "São Paulo", sigla: "SP", investimento: "2,3 milhões", setores: ["Transporte público", "Tecnologia"] },
    { id: 2, estado: "Minas Gerais", sigla: "MG", investimento: "1,1 milhão", setores: ["Educação", "Agropecuário"] },
    { id: 3, estado: "Paraná", sigla: "PR", investimento: "950 mil", setores: ["Alimentício", "Agropecuário"] },
    { id: 4, estado: "Rio de Janeiro", sigla: "RJ", investimento: "910 mil", setores: ["Habitação", "Turismo"] },
    { id: 5, estado: "Santa Catarina", sigla: "SC", investimento: "860 mil", setores: ["Tecnologia"] },
  ];


  const compararInvestimento = (a, b) => {
    const parse = valor => parseFloat(valor.replace(/[^\d,]/g, "").replace(",", "."));
    return parse(b.investimento) - parse(a.investimento);
  };



  //? RETORNANDO A FUNÇÃO PARA ALTERNAR ENTRE GRÁFICO E RANKING
  return (
    <div>
      <nav className="navbar">
        <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
      </nav>

      <div className="BuscaEstado">
        <input
          type="text"
          placeholder="🔍︎ Digite o estado ou sigla"
          value={buscaEstado}
          onChange={handleBuscaChange}
          list="estados-list"
        />
        <datalist id="estados-list">
          {Object.entries(ESTADOS_BR).map(([nome, sigla]) => (
            <option key={sigla} value={nome}>{`${nome} (${sigla})`}</option>
          ))}
        </datalist>
        <BtnBuscaEstado estado={buscaEstado} />
      </div>

      <div className="container-mapa-ranking">
        <div className="mapaBrasil">
          <MapaBrasil style={{ maxWidth: "100%", height: "auto" }} />
        </div>

        <div className="info-container">
          <div className="info-nacional">
            <h1 style={{ color: "#2C006A", textAlign: "center", marginBottom: "1.5rem" }}>
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

      <div className="container-novos-Produtos">
        <div className="novos-Produtos-titulo">
          <h1 style={{ color: "#2C006A" }}>Comparação entre estados</h1>
        </div>
        <div className="forms-Grafico">
          <form>
            <label className="campo-Grafico">Selecione o Estado A: </label>
            <input
              className="select-Grafico"
              type="text"
              list="estados-list"
              name="estadoA"
              placeholder="Digite ou selecione um estado"
            />
            <datalist id="estados-list">
              {Object.entries(ESTADOS_BR).map(([nome, sigla]) => (
                <option key={sigla} value={nome}>
                  {`${nome} (${sigla})`}
                </option>
              ))}
            </datalist>

            <label className="campo-Grafico">Selecione o Estado B: </label>
            <input
              className="select-Grafico"
              type="text"
              list="estados-list"
              name="estadoA"
              placeholder="Digite ou selecione um estado"
            />
            <datalist id="estados-list">
              {Object.entries(ESTADOS_BR).map(([nome, sigla]) => (
                <option key={sigla} value={nome}>
                  {`${nome} (${sigla})`}
                </option>
              ))}
            </datalist>
            <BtnComparar />
          </form>
          <div className="grafico-Comparacao">
            <GraficoTornado />
          </div>
        </div>
      </div>
    </div> // todo fim do return
  );
}
