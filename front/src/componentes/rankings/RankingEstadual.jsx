import React from 'react';

// Esta função não é mais necessária aqui, pois a ordenação vem da API,
// mas se outro componente precisar dela, ela pode ficar.
// const compararFn = ... 

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
        // Calcula a posição global correta para a paginação
        const posicaoGlobal = (page - 1) * perPage + index + 1;

        return (
          <li
            key={item.categoria_padronizada || index} // Usa a categoria como chave ou o index como fallback
            style={{
              borderBottom: '1px solid #ccc',
              padding: '1rem 0',
              color: '#5B228D',
              fontFamily: 'Arial, sans-serif',
            }}
          >
            <div>
              <strong style={{ color: '#cc0066' }}>
                {/* CORREÇÃO DE SINTAXE AQUI: Usando crase para template string */}
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