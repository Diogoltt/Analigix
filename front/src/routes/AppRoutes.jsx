import React from "react";
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from "../pages/Inicio";
import TelaBrasil from '../pages/TelaBrasil';
import TelaEstado from '../pages/TelaEstado';
import PortalTransparencia from '../pages/PortaisTransparencia';

import NotFound from '../pages/NotFound';


export default function AppRoutes(){
    return (
        <Router>
            <Routes>

            <Route path="/analigix" element={<Home />} />
            <Route path="/nacional" element={<TelaBrasil />} />
            <Route path="/estadual/:uf" element={<TelaEstado />} />
            <Route path="/portais-da-Transparencia" element={<PortalTransparencia />} />
            <Route path="*" element={<Home />} />

            </Routes>
        </Router>
    );
}
