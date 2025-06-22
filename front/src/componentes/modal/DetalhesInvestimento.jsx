import React from "react";
import './Detalhes.css';

import { ReactComponent as Moradia } from '../svg/moradia.svg';
import { ReactComponent as Educacao } from '../svg/educacao.svg';
import { ReactComponent as Saude } from '../svg/saude.svg';

export default function DetalhesInvestimento({ isOpen, onClose, item }) {
  if (!isOpen || !item) return null;

  const renderIcon = (categoria) => {
    switch (categoria.toLowerCase()) {
      case "educação":
        return <Educacao style={{ width: "40px", height: "40px" }} />;
      case "saúde":
        return <Saude style={{ width: "40px", height: "40px" }} />;
      case "moradia":
        return <Moradia style={{ width: "40px", height: "40px" }} />;
      default:
        return null;
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✖</button>
        <h2>{item.categoria}</h2>
        {renderIcon(item.categoria)}
        <p><strong>Estado:</strong> {item.sigla}</p>
        <p><strong>Investimento:</strong> {item.investimento}</p>
      </div>
    </div>
  );
}
