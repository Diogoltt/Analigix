import React from "react";

export const ESTADOS_BR = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO"
};
export function buscarEstado(entradaUsuario) {
  if (!entradaUsuario) return null;
  
  const entradaFormatada = entradaUsuario
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();

  for (const [nome, uf] of Object.entries(ESTADOS_BR)) {
    const nomeFormatado = nome
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();

    if (
      nomeFormatado.includes(entradaFormatada) ||
      uf.toLowerCase() === entradaFormatada
    ) {
      return uf;
    }
  }
  return null;
}