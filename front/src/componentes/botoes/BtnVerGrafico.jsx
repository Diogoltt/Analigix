import React from "react";
import './Botoes.css';

export default function BtnVerGrafico({ mostrarGrafico, setMostrarGrafico }) {
  return (
    <button className="btn" onClick={() => setMostrarGrafico(!mostrarGrafico)}>
      {mostrarGrafico ? "Ver Ranking" : "Ver Gráfico"}
    </button>
  );
}
