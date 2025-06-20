import React from 'react';
import './Botoes.css';

export default function BtnSaibaMais({ onClick }) {
  return (
    <button className="btn" onClick={onClick}>
      Conheça Mais
    </button>
  );
}
