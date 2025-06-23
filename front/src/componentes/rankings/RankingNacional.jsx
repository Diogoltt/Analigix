import React from 'react';

// Pequeno dicionário para traduzir a sigla para o nome completo, se precisar.
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

// O componente agora só precisa da prop 'items'. A ordenação já foi feita na API.
const RankingNacional = ({ items }) => {

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {items.map((item, index) => (
        <li
          // A key agora é o estado (sigla), que é único neste ranking.
          key={item.estado}
          style={{
            borderBottom: '1px solid #ccc',
            padding: '1rem 0',
            color: '#5B228D',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          <strong style={{ color: '#cc0066' }}>
            {/* Usamos a sigla (item.estado) para pegar o nome completo no dicionário */}
            {medalhas[index]} - {nomesDosEstados[item.estado]} ({item.estado})
          </strong>
          <div style={{ marginTop: '0.3rem' }}>
            <strong>Investido:</strong> 
            {/* Exibimos o total_investido que veio da API, formatado como moeda */}
            {' R$ ' + (item.total_investido || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </div>

          {/* A API atual não nos diz os setores de destaque, então removemos essa parte por enquanto */}
          {/* <div style={{ marginTop: '0.3rem' }}>
            ° Destaca-se pelo setor de{' '}
            <strong>{item.setores.join(' e ')}</strong>
          </div> */}
        </li>
      ))}
    </ul>
  );
};

export default RankingNacional;