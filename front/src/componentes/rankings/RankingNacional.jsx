import React from 'react';


const nomesDosEstados = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
    'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
    'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
    'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí',
    'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo',
    'SE': 'Sergipe', 'TO': 'Tocantins'
};

const medalhas = ['🥇', '🥈', '🥉', '4°', '5°'];


const RankingNacional = ({ items }) => {

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {items.map((item, index) => (
        <li
          
          key={item.estado}
          style={{
            borderBottom: '1px solid #ccc',
            padding: '1rem 0',
            color: '#5B228D',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          <strong style={{ color: '#cc0066' }}>
            {medalhas[index]} - {nomesDosEstados[item.estado]} ({item.estado})
          </strong>
          <div style={{ marginTop: '0.3rem' }}>
            <strong>Investido:</strong> 
            
            {' R$ ' + (item.total_investido || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </div>
        </li>
      ))}
    </ul>
  );
};

export default RankingNacional;