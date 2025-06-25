import React from "react";
import { buscarEstado } from "../../util/Estados";
import "./Botoes.css";

export default function BtnComparar({ estadoA, estadoB, onComparar }) {
  const handleClick = () => {
    const ufA = buscarEstado(estadoA);
    const ufB = buscarEstado(estadoB);

    if (!ufA || !ufB) {
      alert("Verifique se os dois estados estão preenchidos corretamente.");
      return;
    }

    onComparar(ufA, ufB);
  };

  return (
    <button className="btn" onClick={handleClick} type="button">
      Comparar Estados
    </button>
  );
}
