import React from 'react';

const medalhas = ['🥇', '🥈', '🥉', '4°', '5°'];

const RankingNacional = ({ items, compareFn }) => {
  const sortedItems = [...items].sort(compareFn);

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {sortedItems.map((item, index) => (
        <li
          key={item.id}
          style={{
            borderBottom: '1px solid #ccc',
            padding: '1rem 0',
            color: '#5B228D',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          <strong style={{ color: '#cc0066' }}>
            {medalhas[index]} - {item.estado} ({item.sigla})
          </strong>
          <div style={{ marginTop: '0.3rem' }}>
            <strong>Investido:</strong> {item.investimento}
          </div>
          <div style={{ marginTop: '0.3rem' }}>
            ° Destaca-se pelo setor de{' '}
            <strong>{item.setores.join(' e ')}</strong>
          </div>
        </li>
      ))}
    </ul>
  );
};

export default RankingNacional;
