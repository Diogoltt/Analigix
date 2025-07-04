"""
Sistema de categorização de despesas públicas por área de atuação.
"""

import pandas as pd


def mapear_categoria_padronizada(orgao):
    """
    Mapeia o órgão para uma categoria padronizada baseada na área de atuação.
    Usa sistema de pontuação para priorizar categorias mais específicas.
    """
    if pd.isna(orgao) or orgao is None:
        return 'Outros'
    
    orgao_lower = str(orgao).lower()
    
    categorias_pontuacao = {}
    
    categorias_config = {
        'Tecnologia da Informação e Inovação': {
            'palavras': ['tecnologia', 'informação', 'informacao', 'informa��o', 'informa??o', 'informatica', 'inform�tica', 'inform?tica', 'tic', 'inovação', 'inovacao', 'inova��o', 'inova??o', 'ciência', 'ciencia', 'ci�ncia', 'ci?ncia', 'modernização', 'modernizacao', 'moderniza��o', 'moderniza??o', 'transformação digital', 'transforma��o digital', 'transforma??o digital', 'secretaria de ciência', 'secretaria de ci�ncia', 'secretaria de ci?ncia', 'secretaria de tecnologia'],
            'peso_base': 100,
            'palavras_especificas': ['ciência, tecnologia', 'ci�ncia, tecnologia', 'ci?ncia, tecnologia', 'tecnologia e inovação', 'tecnologia e inova��o', 'tecnologia e inova??o', 'desenvolvimento, ciência, tecnologia', 'inovação, modernização e transformação digital', 'inova��o, moderniza��o e transforma��o digital', 'inova??o, moderniza??o e transforma??o digital']
        },
        'Educação': {
            'palavras': ['educação', 'educacao', 'educa��o', 'educa??o', 'educac?o', 'educaÃ§Ã£o', 'escola', 'colégio', 'colegio', 'col�gio', 'ensino', 'universidade', 'educacional', 'secretaria de educação', 'secretaria de educa��o', 'secretaria de educa??o', 'secretaria da educação', 'secretaria da educa��o', 'secretaria da educa??o', 'fundo de educação', 'fundo de educa��o', 'fundo de educa??o', 'instituto de educação', 'instituto de educa��o', 'instituto de educa??o'],
            'peso_base': 90,
            'palavras_especificas': ['secretaria estadual de educação', 'secretaria estadual de educa��o', 'secretaria estadual de educa??o', 'fundo estadual de educação', 'fundo estadual de educa��o', 'fundo estadual de educa??o', 'secretaria de estado da educa��o', 'secretaria de estado da educa??o']
        },
        'Saúde': {
            'palavras': ['saúde', 'saude', 'sa�de', 'sa?de', 'sauÌde', 'hospital', 'médico', 'medico', 'm�dico', 'm?dico', 'medicamento', 'sus', 'vigilância sanitária', 'vigilancia sanitaria', 'vigil�ncia sanit�ria', 'vigil?ncia sanit?ria', 'fundo de saúde', 'fundo de sa�de', 'fundo de sa?de', 'secretaria de saúde', 'secretaria de sa�de', 'secretaria de sa?de', 'secretaria da saúde', 'secretaria da sa�de', 'secretaria da sa?de'],
            'peso_base': 90,
            'palavras_especificas': ['fundo estadual de saúde', 'fundo estadual de sa�de', 'fundo estadual de sa?de', 'secretaria estadual de saúde', 'secretaria estadual de sa�de', 'secretaria estadual de sa?de', 'secretaria de estado da sa�de', 'secretaria de estado da sa?de']
        },
        'Segurança Pública': {
            'palavras': ['segurança', 'seguranca', 'seguran�a', 'seguran?a', 'seguranã§a', 'polícia', 'policia', 'pol�cia', 'pol?cia', 'bombeiro', 'militar', 'defesa civil', 'penitenciário', 'penitenciario', 'penitenci�rio', 'penitenci?rio', 'presídio', 'presidio', 'pres�dio', 'pres?dio', 'fundo especial de seguran', 'fundo de seguran', 'secretaria de seguran', 'departamento de seguran'],
            'peso_base': 85,
            'palavras_especificas': ['segurança pública', 'seguran�a p�blica', 'seguran?a p?blica', 'defesa civil', 'fundo especial de segurança pública', 'fundo especial de seguran�a p�blica', 'fundo especial de seguran?a p?blica']
        },
        'Infraestrutura e Transporte': {
            'palavras': ['infraestrutura', 'infra-estrutura', 'estrada', 'rodagem', 'transporte', 'obra', 'mobilidade', 'logística', 'logistica'],
            'peso_base': 80,
            'palavras_especificas': ['infraestrutura e logística', 'infraestrutura e transporte']
        },
        'Fazenda e Finanças': {
            'palavras': ['fazenda', 'finanças', 'financas', 'finan�as', 'finan?as', 'tributação', 'tributacao', 'tributa��o', 'tributa??o', 'receita', 'planejamento'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Meio Ambiente': {
            'palavras': ['meio ambiente', 'ambiental', 'floresta', 'sustentabilidade'],
            'peso_base': 70,  
            'palavras_especificas': []
        },
        'Agricultura e Desenvolvimento Rural': {
            'palavras': ['agricultura', 'agraria', 'agrária', 'agr�ria', 'agr?ria', 'rural', 'agropecuária', 'agropecuaria', 'agropecu�ria', 'agropecu?ria', 'desenvolvimento rural', 'sanitária, animal', 'sanit�ria, animal', 'sanit?ria, animal', 'vegetal', 'fitossanitário', 'fitossanit�rio', 'fitossanit?rio', 'pecuária', 'pecuaria', 'pecu�ria', 'pecu?ria', 'defesa sanitária', 'defesa sanit�ria', 'defesa sanit?ria'],
            'peso_base': 75,
            'palavras_especificas': ['defesa sanitária, animal e vegetal', 'defesa sanit�ria, animal e vegetal', 'defesa sanit?ria, animal e vegetal', 'sanitária, animal e vegetal', 'sanit�ria, animal e vegetal', 'sanit?ria, animal e vegetal']
        },
        'Assistência Social': {
            'palavras': ['social', 'assistência', 'assistencia', 'assist�ncia', 'assist?ncia', 'cidadania', 'família', 'familia', 'fam�lia', 'fam?lia'],
            'peso_base': 65,
            'palavras_especificas': []
        },
        'Cultura, Esporte e Turismo': {
            'palavras': ['turismo', 'cultura', 'esporte', 'lazer'],
            'peso_base': 70,
            'palavras_especificas': []
        },
        'Habitação e Urbanismo': {
            'palavras': ['habitação','habitacao', 'habita��o', 'habita??o', 'habitac?o', 'moradia', 'urbanismo', 'cidade', 'desenvolvimento urbano'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Trabalho e Emprego': {
            'palavras': ['trabalho', 'emprego', 'qualificação', 'qualificacao', 'qualifica��o', 'qualifica??o', 'profissionalização', 'profissionalizacao', 'profissionaliza��o', 'profissionaliza??o', 'carteira assinada'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Indústria e Comércio': {
            'palavras': ['indústria', 'industria', 'ind�stria', 'ind?stria', 'industrial', 'comércio', 'comercio', 'com�rcio', 'com?rcio', 'junta comercial', 'desenvolvimento econômico', 'desenvolvimento economico', 'desenvolvimento econ�mico', 'desenvolvimento econ?mico', 'empreendedorismo'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Saneamento e Recursos Hídricos': {
            'palavras': ['saneamento', 'água', 'agua', '�gua', '?gua', 'esgoto', 'hídrico', 'hidrico', 'h�drico', 'h?drico', 'recursos hídricos', 'recursos h�dricos', 'recursos h?dricos'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Direitos Humanos e Igualdade': {
            'palavras': ['direitos humanos', 'igualdade', 'diversidade', 'mulher', 'racial', 'gênero', 'genero', 'g�nero', 'g?nero'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Energia': {
            'palavras': ['energia', 'energética', 'energetica', 'energ�tica', 'energ?tica'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Comunicação': {
            'palavras': ['comunicação', 'comunicacao', 'comunica��o', 'comunica??o', 'rádio', 'radio', 'r�dio', 'r?dio', 'televisão', 'televisao', 'televis�o', 'televis?o'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Administração e Gestão Pública': {
            'palavras': ['administração', 'administracao', 'administra��o', 'administra??o', 'administrac?o', 'gestão', 'gestao', 'gest�o', 'gest?o', 'servidor', 'recursos humanos', 'rh', 'pessoal', 'administração pública', 'administra��o p�blica', 'administra??o p?blica', 'casa civil', 'gabinete', 'governadoria', 'secretaria de administração', 'secretaria de administra��o', 'secretaria de administra??o', 'administra��o geral', 'administra??o geral'],
            'peso_base': 50,  
            'palavras_especificas': ['administração geral', 'administra��o geral', 'administra??o geral', 'administrac?o geral', 'administra��o geral do estado', 'administra??o geral do estado', 'casa civil', 'secretaria de administração e previdência', 'secretaria de administra��o e previd�ncia', 'secretaria de administra??o e previd?ncia', 'secretaria de estado da administra��o', 'secretaria de estado da administra??o']
        },
        'Poder Legislativo': {
            'palavras': ['legislativa', 'assembleia', 'câmara', 'camara', 'c�mara', 'c?mara'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Poder Judiciário': {
            'palavras': ['judiciário', 'judiciario', 'judici�rio', 'judici?rio', 'judiciária', 'judiciaria', 'judici�ria', 'judici?ria', 'tribunal', 'justiça', 'justica', 'justi�a', 'justi?a'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Ministério Público e Controle': {
            'palavras': ['ministério público', 'ministerio publico', 'minist�rio p�blico', 'minist?rio p?blico', 'mp', 'controle externo'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Administração Geral': {
            'palavras': ['governadoria', 'gabinete', 'casa civil'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Reserva de Contingência': {
            'palavras': ['reserva', 'contingência', 'contingencia', 'conting�ncia', 'conting?ncia'],
            'peso_base': 90,
            'palavras_especificas': []
        },
        'Encargos da Dívida': {
            'palavras': ['dívida', 'divida', 'd�vida', 'd?vida', 'encargo', 'financiamento', 'amortização', 'amortizacao', 'amortiza��o', 'amortiza??o'],
            'peso_base': 85,
            'palavras_especificas': []
        }
    }
    
    # Calcular pontuação para cada categoria
    for categoria, config in categorias_config.items():
        pontuacao = 0
        
        # Verificar palavras específicas (maior peso)
        for palavra_especifica in config['palavras_especificas']:
            if palavra_especifica in orgao_lower:
                pontuacao += config['peso_base'] * 2  
        
        # Verificar palavras gerais
        for palavra in config['palavras']:
            if palavra in orgao_lower:
                pontuacao += config['peso_base']
        
        if pontuacao > 0:
            categorias_pontuacao[categoria] = pontuacao
    
    # Retornar categoria com maior pontuação
    if categorias_pontuacao:
        categoria_escolhida = max(categorias_pontuacao.items(), key=lambda x: x[1])
        return categoria_escolhida[0]
    
    return 'Outros'


def limpar_caracteres_especiais(texto):
    """
    Retorna o texto original sem nenhuma modificação.
    A categorização vai trabalhar diretamente com os caracteres corrompidos.
    """
    if pd.isna(texto) or texto is None:
        return texto
    
    return str(texto).strip()
