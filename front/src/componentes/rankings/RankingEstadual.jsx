import React, { useState } from 'react';
import '../botoes/Botoes.css';
import DetalhesInvestimento from '../modal/DetalhesInvestimento';

const RankingEstadual = ({ items, page, perPage, uf, ano }) => {
    const [itemSelecionado, setItemSelecionado] = useState(null);

    if (!items || items.length === 0) {
        return (
            <p style={{ textAlign: 'center', color: '#555' }}>
                Nenhum dado encontrado para este filtro.
            </p>
        );
    }

    const abrirModal = (item) => setItemSelecionado(item);
    const fecharModal = () => setItemSelecionado(null);

    return (
        <>
            <ul style={{ listStyle: 'none', padding: 0 }}>
                {items.map((item, index) => {
                    const posicaoGlobal = (page - 1) * perPage + index + 1;

                    return (
                        <li
                            key={item.categoria_padronizada || index}
                            style={{
                                borderBottom: '1px solid #ccc',
                                padding: '1rem 0',
                                color: '#5B228D',
                                fontFamily: 'Arial, sans-serif',
                            }}
                        >
                            <div
                                style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    flexWrap: 'wrap',
                                    gap: '1rem',
                                }}
                            >
                                <div>
                                    <strong style={{ color: '#cc0066' }}>
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

                                <button className="btn" onClick={() => abrirModal(item)}>Ver Mais</button>
                            </div>
                        </li>
                    );
                })}
            </ul>

            {itemSelecionado && (
                <DetalhesInvestimento
                    isOpen={true}
                    onClose={fecharModal}
                    item={itemSelecionado}
                    uf={uf}
                    ano={ano}
                />
            )}
        </>
    );
};

export default RankingEstadual;