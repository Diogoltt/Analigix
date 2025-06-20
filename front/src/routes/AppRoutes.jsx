import React from "react";
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from "../pages/Inicio";
import TelaBrasil from '../pages/TelaBrasil';
import TelaEstado from '../pages/TelaEstado';
import NotFound from '../pages/NotFound';


export default function AppRoutes(){
    return (
        <Router>
            <Routes>

            <Route path="/analigix" element={<Home />} />
            <Route path="/nacional" element={<TelaBrasil />} />
            <Route path="/estadual/:uf" element={<TelaEstado />} /> //* qualquer caminho que eu clicar ele vai levar a mesma TelaEstado MAS vai carregar as informaçoes dinamicamente
            <Route path="*" element={<NotFound />} />

            </Routes>
        </Router>
    );
}
