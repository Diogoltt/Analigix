import { useParams } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import './css/TelaEstado.css';

import { ReactComponent as LogoAnaligixAzul } from '../componentes/logo/logoAnaligixAzul.svg';
import { ReactComponent as AlfineteMapa } from '../componentes/svg/alfinete.svg';
import { ReactComponent as Filtro } from '../componentes/svg/filtro.svg';

import BtnVoltar from '../componentes/botoes/BtnVoltarTela.jsx';
import RankingEstadual from '../componentes/rankings/RankingEstadual.jsx';

import GraficoPerfil from "../componentes/graficos/GraficoPerfil.jsx";

//? Estados:
import MapaAC from '../componentes/mapas/Acre.jsx';
import MapaAL from '../componentes/mapas/Alagoas.jsx';
import MapaAP from '../componentes/mapas/Amapa.jsx';
import MapaAM from '../componentes/mapas/Amazonas.jsx';
import MapaBA from '../componentes/mapas/Bahia.jsx';
import MapaCE from '../componentes/mapas/Ceara.jsx';
import MapaDF from '../componentes/mapas/Distrito-Federal.jsx';
import MapaES from '../componentes/mapas/Espirito-Santo.jsx';
import MapaGO from '../componentes/mapas/Goias.jsx';
import MapaMA from '../componentes/mapas/Maranhao.jsx';
import MapaMT from '../componentes/mapas/Mato-Grosso.jsx';
import MapaMS from '../componentes/mapas/Mato-Grosso-do-Sul.jsx';
import MapaMG from '../componentes/mapas/Minas-Gerais.jsx';
import MapaPA from '../componentes/mapas/Para.jsx';
import MapaPB from '../componentes/mapas/Paraiba.jsx';
import MapaPR from '../componentes/mapas/Parana.jsx';
import MapaPE from '../componentes/mapas/Pernambuco.jsx';
import MapaPI from '../componentes/mapas/Piaui.jsx';
import MapaRJ from '../componentes/mapas/Rio-de-Janeiro.jsx';
import MapaRN from '../componentes/mapas/Rio-Grande-do-Norte.jsx';
import MapaRS from '../componentes/mapas/Rio-Grande-do-Sul.jsx';
import MapaRO from '../componentes/mapas/Rondonia.jsx';
import MapaRR from '../componentes/mapas/Roraima.jsx';
import MapaSC from '../componentes/mapas/Santa-Catarina.jsx';
import MapaSP from '../componentes/mapas/Sao-Paulo.jsx';
import MapaSE from '../componentes/mapas/Sergipe.jsx';
import MapaTO from '../componentes/mapas/Tocantins.jsx';



export default function TelaEstado() {
    const { uf } = useParams();


    const Exemplo = [
        { id: 1, categoria: "Educação", sigla: "MS", investimento: "R$ 1.000.000" },
        { id: 2, categoria: "Saúde", sigla: "MS", investimento: "R$ 800.000" },
        { id: 3, categoria: "Infraestrutura", sigla: "MS", investimento: "R$ 700.000" },
        { id: 4, categoria: "#", sigla: "MS", investimento: "R$ 700.000" },
        { id: 5, categoria: "#", sigla: "MS", investimento: "R$ 700.000" },
    ];

    const navigate = useNavigate();
    const handleClick = () => navigate("/nacional");

    const mapas = {
        AC: MapaAC, AL: MapaAL, AP: MapaAP, AM: MapaAM, BA: MapaBA,
        CE: MapaCE, DF: MapaDF, ES: MapaES, GO: MapaGO, MA: MapaMA,
        MT: MapaMT, MS: MapaMS, MG: MapaMG, PA: MapaPA, PB: MapaPB,
        PR: MapaPR, PE: MapaPE, PI: MapaPI, RJ: MapaRJ, RN: MapaRN,
        RS: MapaRS, RO: MapaRO, RR: MapaRR, SC: MapaSC, SP: MapaSP,
        SE: MapaSE, TO: MapaTO,
    };

    const MapaComponente = mapas[uf];

    return (
        <div>
            <nav className="navbar">
                <a href="/nacional"><LogoAnaligixAzul width="200px" height="80px" /></a>
            </nav>
            <div className='container-Principal'>
                <div className="container-1">
                    <div className='btnVoltar'>
                        <BtnVoltar texto="Voltar" onClick={handleClick} />
                    </div>
                    <div className="nome-Estado-Filtro">
                        <h1 style={{ color: "#2C006A" }}>
                            <AlfineteMapa />
                            {uf}
                        </h1>

                        {/* Filtro Ano */}
                        <Filtro className="icon" />
                        <select className="filtro" name="ano" id="ano">
                            <option value="">Selecione o ano</option>
                            <option value="2025">2025</option>
                            <option value="2024">2024</option>
                            {/* mais anos aqui */}
                        </select>

                        {/* Filtro Categoria */}
                        <Filtro className="icon" />
                        <select className="filtro" name="categoria" id="categoria">
                            <option value="">Selecione a categoria</option>
                            <option value="saude">Saúde</option>
                            <option value="educacao">Educação</option>
                            <option value="infraestrutura">Infraestrutura</option>
                            {/* mais categorias aqui */}
                        </select>
                    </div>

                    <div className='ranking-Estadual'>
                        <RankingEstadual
                            items={Exemplo}
                            compareFn={(a, b) => b.investimento.localeCompare(a.investimento)}
                        />
                    </div>
                </div>

                <div className='container-2'>
                    <div className='mapa-Estado'>
                        {MapaComponente ? <MapaComponente className="mapa-Estado-Svg" /> : <p>Mapa não disponível</p>}
                    </div>
                    <div className='grafico-Estado'>
                        <GraficoPerfil />
                    </div>
                </div>
            </div>
        </div>
    );
}