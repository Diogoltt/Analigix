import React from "react";
import { useNavigate } from "react-router-dom";
import TelaBrasil from "../pages/TelaBrasil";

import BtnSaibaMais from "../componentes/botoes/BtnSaibaMais";
import { ReactComponent as LogoAnaligix } from '../componentes/logo/logoAnaligix.svg';



export default function Home() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate("/nacional")
  };

  return (
    <div className="container" style={{
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",     
      padding: "20px",
      height: "100vh",          
      boxSizing: "border-box"
    }}>
      <div className="Logo" style={{
        display: "flex",
        alignItems: "center",
        marginBottom: "20px"
      }}>
        <LogoAnaligix />
      </div>
      <p style={{
        textAlign: "center",
        maxWidth: "600px",  
        marginBottom: "20px",
        fontFamily: "Inter, sans-serif",
        fontSize: "18px",
        lineHeight: "1.6"
      }}>
        Conheça o <strong style={{ color: "#5B228D" }}>Analigix</strong> — uma proposta de sistema web desenvolvida para te ajudar a entender e explorar os investimentos realizados no Brasil e em seus estados, por meio de gráficos interativos e rankings detalhados.
      </p>
      <BtnSaibaMais texto="Clique aqui" onClick={handleClick} />
    </div>
  );
}