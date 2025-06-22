import React from 'react';
import './Botoes.css';

export default function BtnVoltar({ onClick }) {
  return (
    <button className="btn" onClick={onClick}>
      Voltar a Tela Nacional
    </button>
  );
}
