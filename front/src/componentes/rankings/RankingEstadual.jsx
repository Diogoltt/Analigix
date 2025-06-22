import React, { useState } from "react";
import '../botoes/Botoes.css';

import DetalhesInvestimento from "../modal/DetalhesInvestimento";

const posicoes = ["1°", "2°", "3°", "4°", "5°"];

const RankingEstadual = ({ items, compareFn }) => {
  const sortedItems = [...items].sort(compareFn);

  const [itemSelecionado, setItemSelecionado] = useState(null);

  const abrirModal = (item) => setItemSelecionado(item);
  const fecharModal = () => setItemSelecionado(null);

  return (
    <>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {sortedItems.map((item, index) => (
          <li
            key={item.id}
            style={{
              borderBottom: "1px solid #ccc",
              padding: "1rem 0",
              color: "#5B228D",
              fontFamily: "Arial, sans-serif",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <strong style={{ color: "#cc0066" }}>
                {posicoes[index]} - {item.categoria} ({item.sigla})
              </strong>
              <div style={{ marginTop: "0.3rem" }}>
                <strong>Investido:</strong> {item.investimento}
              </div>
            </div>

            <button className="btn" onClick={() => abrirModal(item)}>Ver Mais</button>
          </li>
        ))}
      </ul>

      {itemSelecionado && (
        <DetalhesInvestimento
          isOpen={true}
          onClose={fecharModal}
          item={itemSelecionado}
        />
      )}
    </>
  );
};

export default RankingEstadual;
