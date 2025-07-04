import React from "react";
import { useNavigate } from "react-router-dom";
import "./Botoes.css";
import { buscarEstado } from '../../util/Estados';

export default function BtnBuscaEstado({ estado }) {
  const navigate = useNavigate();

  const handleClick = () => {
    const uf = buscarEstado(estado);
    if (uf) {
      navigate(`/estadual/${uf}`);
      console.log(`Navegando para /estadual/${uf}`);
    }
    else{
      alert("Estado não encontrado. Digite o nome completo ou sigla (ex: São Paulo ou SP)");
    }
  };

  return (
    <button className="btn" onClick={handleClick}>
      Buscar
    </button>
  );
}