import React from 'react';
const RankingEstadual = ({ items, page, perPage }) => {
  if (!items || items.length === 0) {
    return (
      <p style={{ textAlign: 'center', color: '#555' }}>
        Nenhum dado encontrado para este filtro.
      </p>
    );
  }

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {items.map((item, index) => {
        const posicaoGlobal = (page - 1) * perPage + index + 1;

        return (
          <li
            key={item.categoria_padronizada}
            style={{
              borderBottom: '1px solid #ccc',
              padding: '1rem 0',
              color: '#5B228D',
              fontFamily: 'Arial, sans-serif',
            }}
          >
            <div>
              <strong style={{ color: '#cc0066' }}>
                {/* Usando a nova variável para a posição correta */}
                {`${posicaoGlobal}°`} - {item.categoria_padronizada}
              </strong>
              <div style={{ marginTop: '0.3rem' }}>
                <strong>Investido:</strong>
                {' R$ ' +
                  (item.total_gasto || 0).toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
};

export default RankingEstadual;
