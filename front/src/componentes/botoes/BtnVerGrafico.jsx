import React from "react";
import './Botoes.css';

export default function BtnVerGrafico({ mostrarGrafico, setMostrarGrafico, disabled = false }) {
  return (
    <button 
      className="btn" 
      onClick={() => !disabled && setMostrarGrafico(!mostrarGrafico)}
      disabled={disabled}
      style={disabled ? { opacity: 0.5, cursor: 'not-allowed' } : {}}
    >
      {mostrarGrafico ? "Ver Ranking" : "Ver Gráfico"}
    </button>
  );
}
