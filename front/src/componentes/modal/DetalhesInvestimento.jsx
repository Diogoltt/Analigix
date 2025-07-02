import React, { useState, useEffect } from 'react';
import './Detalhes.css';

const formatarMoeda = (valor) => {
    if (typeof valor !== 'number') return 'R$ 0,00';
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

export default function DetalhesInvestimento({ isOpen, onClose, item, uf, ano }) {
    const [detalhesData, setDetalhesData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!isOpen || !item || !uf) return;

        const fetchDetalhes = async () => {
            setLoading(true);
            
            const params = new URLSearchParams();
            params.append('uf', uf);
            // CORRIGIDO DE VOLTA: Usa a chave correta que vem do componente de Ranking
            params.append('categoria', item.categoria_padronizada); 
            if (ano) {
                params.append('ano', ano);
            }
            
            const apiUrl = `http://127.0.0.1:5000/api/detalhes-categoria?${params.toString()}`;

            try {
                const response = await fetch(apiUrl);
                const data = await response.json();
                if (data.error) throw new Error(data.error);
                
                const linhasFormatadas = data.map(detalhe => ({
                    indicador: detalhe.orgao,
                    valor: formatarMoeda(detalhe.total_por_orgao)
                }));
                setDetalhesData(linhasFormatadas);
            } catch (error) {
                console.error("Erro ao buscar detalhes da categoria:", error);
                setDetalhesData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchDetalhes();
    }, [isOpen, item, uf, ano]);

    if (!isOpen || !item) return null;

    const renderTabelaDetalhamento = (linhas) => {
        if (loading) return <p>Carregando detalhes...</p>;
        if (!linhas || linhas.length === 0) return <p>Nenhum detalhamento encontrado.</p>;

        return (
            <div className="tabela-container">
                <table className="tabela-detalhes">
                    <thead className='tabela-header'>
                        <tr>
                            <th>Órgão</th>
                            <th>Valor Gasto (Total)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {linhas.map((linha, index) => (
                            <tr key={index}>
                                <td>{linha.indicador}</td>
                                <td>{linha.valor}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose}>✖</button>
                
                {/* CORRIGIDO DE VOLTA: Usa a chave correta que vem do componente de Ranking */}
                <h2>{item.categoria_padronizada}</h2>
                
                <p className="info-modal">
                    <strong>Total na Categoria:</strong> {formatarMoeda(item.total_gasto)}
                </p>
                {renderTabelaDetalhamento(detalhesData)}
            </div>
        </div>
    );
}