import React, { useState } from 'react';
import './css/PortalTransparencia.css';
import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { useNavigate } from "react-router-dom";
import BtnVoltar from '../componentes/botoes/BtnVoltarTela.jsx';


const portaisEstaduais = [

    { nome: 'Acre', uf: 'AC', url: 'https://transparencia.ac.gov.br/despesas' },
    { nome: 'Alagoas', uf: 'AL', url: ' https://transparencia.al.gov.br/despesa/despesas-por-orgao/' },
    { nome: 'Amapá', uf: 'AP', url: 'http://www.transparencia.ap.gov.br/informacoes/dados-aberto' },
    { nome: 'Amazonas', uf: 'AM', url: 'https://www.transparencia.am.gov.br/despesas/' },
    { nome: 'Bahia', uf: 'BA', url: 'https://www.transparencia.ba.gov.br/Despesa/Painel' },
    { nome: 'Ceará', uf: 'CE', url: 'https://acesse.one/V0nmL' },
    { nome: 'Distrito Federal', uf: 'DF', url: 'https://www.transparencia.df.gov.br/#/despesas/orgao' },
    { nome: 'Espírito Santo', uf: 'ES', url: 'https://transparencia.es.gov.br/Despesa' },
    { nome: 'Goiás', uf: 'GO', url: 'https://transparencia.go.gov.br/gastos-governamentais/' },
    { nome: 'Mato Grosso', uf: 'MT', url: 'https://consultas.transparencia.mt.gov.br/despesa/detalhada/' },
    { nome: 'Mato Grosso do Sul', uf: 'MS', url: 'https://www.transparencia.ms.gov.br/#/Despesa' },
    { nome: 'Minas Gerais', uf: 'MG', url: 'https://www.transparencia.mg.gov.br/despesa-estado/despesa' },
    { nome: 'Pará', uf: 'PA', url: 'https://www.sistemas.pa.gov.br/portaltransparencia/empenho/notas' },
    { nome: 'Paraíba', uf: 'PB', url: 'https://transparencia.pb.gov.br/despesas/despesa-orcamentaria' },
    { nome: 'Paraná', uf: 'PR', url: 'https://www.transparencia.pr.gov.br/pte/assunto/4/287?origem=3' },
    { nome: 'Piauí', uf: 'PI', url: 'https://transparencia2.pi.gov.br/despesas' },
    { nome: 'Rio de Janeiro', uf: 'RJ', url: 'http://www.transparencia.rj.gov.br/' },
    { nome: 'Rio Grande do Norte', uf: 'RN', url: 'http://www.transparencia.rn.gov.br/gastos-diretos' },
    { nome: 'Rio Grande do Sul', uf: 'RS', url: 'https://transparencia.rs.gov.br/' },
    { nome: 'Rondônia', uf: 'RO', url: 'https://transparencia.ro.gov.br/despesa/despesa-estadual' },
    { nome: 'Roraima', uf: 'RR', url: 'https://transparencia.rr.gov.br/quadrodetalhamentodespesa' },
    { nome: 'Santa Catarina', uf: 'SC', url: ' https://www.transparencia.sc.gov.br/despesa' },
    { nome: 'São Paulo', uf: 'SP', url: 'https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/FlexConsDespesa.aspx' },
    { nome: 'Tocantins', uf: 'TO', url: 'https://transparencia.to.gov.br/despesas' },
];



export default function PortalTransparencia() {
    const navigate = useNavigate();
    const handleClick = () => navigate("/nacional");

    const [estadoSelecionado, setEstadoSelecionado] = useState('');
    const [anoSelecionado, setAnoSelecionado] = useState('');
    const [nomeArquivo, setNomeArquivo] = useState('');
    const [isDragOver, setIsDragOver] = useState(false);

    const handleFileChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            const file = event.target.files[0];
            if (validateFile(file)) {
                setNomeArquivo(file.name);
            }
        } else {
            setNomeArquivo('');
        }
    };

    const validateFile = (file) => {
        if (!file.name.toLowerCase().endsWith('.csv')) {
            alert("Por favor, selecione apenas arquivos CSV.");
            return false;
        }
        return true;
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (event) => {
        event.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setIsDragOver(false);
        
        const files = event.dataTransfer.files;
        if (files && files[0]) {
            const file = files[0];
            if (validateFile(file)) {
                setNomeArquivo(file.name);
                const inputFile = document.getElementById("csv-upload");
                inputFile.files = files;
            }
        }
    };

    const handleCancelarArquivo = (event) => {
        event.preventDefault();
        event.stopPropagation();
        setNomeArquivo('');
        document.getElementById("csv-upload").value = '';
    };


    const handleBuscaClick = async () => {
        if (!estadoSelecionado || !anoSelecionado || !nomeArquivo) {
            alert("Por favor, selecione estado, ano e um arquivo CSV.");
            return;
        }

        const inputFile = document.getElementById("csv-upload");
        const file = inputFile.files[0];

        if (!file.name.toLowerCase().endsWith('.csv')) {
            alert("Por favor, selecione apenas arquivos CSV.");
            return;
        }

        const formData = new FormData();
        formData.append("estado", estadoSelecionado);
        formData.append("ano", anoSelecionado);
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.erro || 'Erro desconhecido');
            }

            alert(`Arquivo enviado com sucesso! Salvo como: ${result.arquivo}`);

            setEstadoSelecionado('');
            setAnoSelecionado('');
            setNomeArquivo('');
            document.getElementById("csv-upload").value = '';

        } catch (error) {
            alert(`Erro ao enviar arquivo: ${error.message}`);
        }
    };
return (
    <div>
        <nav className="navbar">
            <a href="/analigix"><LogoAnaligixAzul width="200px" height="80px" /></a>
            <div className="nav-links">
                <a href="/nacional" style={{ color: "white" }}>Dashboard</a>
                <a href="/tendencias" style={{ color: "white" }}>Tendências</a>
            </div>
        </nav>
        <div className='container-Principal'>
            <div className='btnVoltar'>
                <BtnVoltar texto="Voltar" onClick={handleClick} />
            </div>
        </div>
        <div className="portal-container">

            <div className="coluna-portais">
                <h2 className="titulo-coluna" style={{color: '#5B228D'}}>Portais da Transparência</h2>
                <div className="lista-portais">
                    {portaisEstaduais.map((estado) => (
                        <a
                            key={estado.uf}
                            href={estado.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="link-portal"
                        >
                            <span className="link-portal-uf" style={{color: '#0EC0D1'}}>{estado.uf}</span>
                            <span className="link-portal-nome">{estado.nome}</span>
                            <span className="link-portal-icone">→</span>
                        </a>
                    ))}
                </div>
            </div>

            <aside className="coluna-acoes">
                <div className="caixa-aviso">
                    <span className="aviso-icone">⚠️</span>
                    <div className="aviso-texto">
                        <strong>Atenção:</strong> Os estados do Maranhão (MA), Pernambuco (PE) e Sergipe (SE) ainda não possuem suporte para análise automática.
                    </div>
                </div>

                <div className="box-acoes">
                    <h2 className="titulo-coluna" style={{color: '#5B228D'}}>Área de Ações</h2>

                    <label htmlFor="estado-select" className="label-filtro">Selecione o Estado</label>
                    <select
                        id="estado-select"
                        value={estadoSelecionado}
                        onChange={(e) => setEstadoSelecionado(e.target.value)}
                        className="seletor-filtro"
                    >
                        <option value="">-- Selecione um Estado --</option>
                        {portaisEstaduais.map((estado) => (
                            <option key={estado.uf} value={estado.uf}>{estado.nome}</option>
                        ))}
                    </select>

                    <label htmlFor="ano-select" className="label-filtro">Selecione o Ano</label>
                    <select
                        id="ano-select"
                        value={anoSelecionado}
                        onChange={(e) => setAnoSelecionado(e.target.value)}
                        className="seletor-filtro"
                    >
                        <option value="">-- Selecione um Ano --</option>
                        <option value="2025">2025</option>
                        <option value="2024">2024</option>
                        <option value="2023">2023</option>
                        <option value="2022">2022</option>
                        <option value="2021">2021</option>
                        <option value="2020">2020</option>
                    </select>

                    <label htmlFor="csv-upload" className="label-filtro">Anexar Arquivo CSV</label>
                    <div 
                        className={`upload-box ${isDragOver ? 'drag-over' : ''}`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                    >
                        <input
                            type="file"
                            id="csv-upload"
                            className="upload-input"
                            accept=".csv"
                            onChange={handleFileChange}
                        />
                        <label htmlFor="csv-upload" className="upload-label">
                            {nomeArquivo ? (
                                <div className="arquivo-selecionado">
                                    <span className="upload-texto">{nomeArquivo}</span>
                                    <button 
                                        type="button"
                                        onClick={handleCancelarArquivo}
                                        className="botao-cancelar-arquivo"
                                        title="Remover arquivo"
                                    >
                                        ✕
                                    </button>
                                </div>
                            ) : (
                                <>
                                    <span className="upload-icone">📤</span>
                                    <div className="upload-texto">
                                        Arraste e solte o arquivo aqui ou <br />
                                        <span className="upload-texto-destaque">clique para selecionar</span>
                                    </div>
                                </>
                            )}
                        </label>
                    </div>

                    <button onClick={handleBuscaClick} className="botao-buscar">
                        Enviar
                    </button>
                </div>
            </aside>
        </div>
    </div>
);
}


