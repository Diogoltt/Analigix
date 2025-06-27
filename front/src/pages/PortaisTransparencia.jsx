import React, { useState } from 'react';
import './css/PortalTransparencia.css';



const portaisEstaduais = [
    
  { nome: 'Acre', uf: 'AC', url: 'https://transparencia.ac.gov.br/' },
  { nome: 'Alagoas', uf: 'AL', url: 'http://transparencia.al.gov.br/' },
  { nome: 'Amapá', uf: 'AP', url: 'https://transparencia.ap.gov.br/' },
  { nome: 'Amazonas', uf: 'AM', url: 'http://www.transparencia.am.gov.br/' },
  { nome: 'Bahia', uf: 'BA', url: 'http://www.transparencia.ba.gov.br/' },
  { nome: 'Ceará', uf: 'CE', url: 'https://cearatransparente.ce.gov.br/' },
  { nome: 'Distrito Federal', uf: 'DF', url: 'http://www.transparencia.df.gov.br/' },
  { nome: 'Espírito Santo', uf: 'ES', url: 'https://transparencia.es.gov.br/' },
  { nome: 'Goiás', uf: 'GO', url: 'https://goias.gov.br/transparencia/' },
  { nome: 'Maranhão', uf: 'MA', url: 'http://www.transparencia.ma.gov.br/' },
  { nome: 'Mato Grosso', uf: 'MT', url: 'http://www.transparenciamatogrosso.mt.gov.br/' },
  { nome: 'Mato Grosso do Sul', uf: 'MS', url: 'https://www.transparencia.ms.gov.br/' },
  { nome: 'Minas Gerais', uf: 'MG', url: 'http://www.transparencia.mg.gov.br/' },
  { nome: 'Pará', uf: 'PA', url: 'https://www.transparencia.pa.gov.br/' },
  { nome: 'Paraíba', uf: 'PB', url: 'https://transparencia.pb.gov.br/' },
  { nome: 'Paraná', uf: 'PR', url: 'http://www.transparencia.pr.gov.br/' },
  { nome: 'Pernambuco', uf: 'PE', url: 'https://www.transparencia.pe.gov.br/' },
  { nome: 'Piauí', uf: 'PI', url: 'http://www.transparencia.pi.gov.br/' },
  { nome: 'Rio de Janeiro', uf: 'RJ', url: 'http://www.transparencia.rj.gov.br/' },
  { nome: 'Rio Grande do Norte', uf: 'RN', url: 'http://www.transparencia.rn.gov.br/' },
  { nome: 'Rio Grande do Sul', uf: 'RS', url: 'https://transparencia.rs.gov.br/' },
  { nome: 'Rondônia', uf: 'RO', url: 'https://transparencia.ro.gov.br/' },
  { nome: 'Roraima', uf: 'RR', url: 'https://www.transparencia.rr.gov.br/' },
  { nome: 'Santa Catarina', uf: 'SC', url: 'http://www.transparencia.sc.gov.br/' },
  { nome: 'São Paulo', uf: 'SP', url: 'http://www.transparencia.sp.gov.br/' },
  { nome: 'Sergipe', uf: 'SE', url: 'https://sergipe.se.gov.br/transparencia-sergipe/' },
  { nome: 'Tocantins', uf: 'TO', url: 'https://transparencia.to.gov.br/' },
];

export default function PortalTransparencia() {
  const [estadoSelecionado, setEstadoSelecionado] = useState('');
  const [anoSelecionado, setAnoSelecionado] = useState('');
  const [nomeArquivo, setNomeArquivo] = useState('');

  const [file, setFile] = useState(null);
  
  const handleFileChange = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    setFile(selectedFile);
    setNomeArquivo(selectedFile.name);
  } else {
    setFile(null);
    setNomeArquivo('');
  }
};


  const handleBuscaClick = async () => {
  if (!estadoSelecionado || !anoSelecionado) {
    alert('Selecione um estado e um ano antes de continuar.');
    return;
  }

  const formData = new FormData();
  formData.append('estado', estadoSelecionado);
  formData.append('ano', anoSelecionado);

  if (file) {
    formData.append('file', file);
  }

  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      alert('Arquivo enviado com sucesso!');
    } else {
      alert('Erro ao enviar o arquivo.');
    }
  } catch (error) {
    console.error('Erro ao enviar:', error);
    alert('Erro de conexão com o servidor.');
  }
};


  return (
    <div className="portal-container">
      {/* Coluna da Esquerda (Lista de Links) */}
      <div className="coluna-portais">
        <h2 className="titulo-coluna">Portais da Transparência</h2>
        <div className="lista-portais">
          {portaisEstaduais.map((estado) => (
            <a 
              key={estado.uf} 
              href={estado.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="link-portal"
            >
              <span className="link-portal-uf">{estado.uf}</span>
              <span className="link-portal-nome">{estado.nome}</span>
              <span className="link-portal-icone">→</span>
            </a>
          ))}
        </div>
      </div>

      <aside className="coluna-acoes">
        <h2 className="titulo-coluna">Área de Ações</h2>
        <div className="box-acoes">
          
          
          
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

          {/* Filtro de Ano */}
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
          </select>

         
          <label htmlFor="csv-upload" className="label-filtro">Anexar Arquivo CSV (Opcional)</label>
            <div className="upload-box">
            <input 
                type="file" 
                id="csv-upload" 
                className="upload-input" 
                accept=".csv"
                onChange={handleFileChange}
            />
            <label htmlFor="csv-upload" className="upload-label">
               
                {nomeArquivo ? (
                <span className="upload-texto">{nomeArquivo}</span>
                ) : (
                <>
                    <span className="upload-icone">📤</span>
                    <div className="upload-texto">
                    Arraste e solte o arquivo aqui ou <br/>
                    <span className="upload-texto-destaque">clique para selecionar</span>
                    </div>
                </>
                )}
            </label>
            </div>
          
          {/* Botão de Buscar */}
          <button onClick={handleBuscaClick} className="botao-buscar">
            Buscar
          </button>
        </div>
      </aside>
    </div>
  );
}