# Padrões Normativos M7 — Referência Completa

Extraído da POL-M7-001: Política de Gestão por Processos e Padronização.

## Hierarquia Normativa

| Nível | Código | Tipo | Pergunta que Responde | Público-Alvo | Aprovador |
|-------|--------|------|----------------------|--------------|-----------|
| Estratégico | POL | Política | "Por quê e dentro de quais limites?" | Toda a organização | Diretoria |
| Tático | MAN | Manual | "O que fazer e o que esperar?" | Gestores e líderes | Head de área |
| Operacional | INS | Instrução | "Como fazer, passo a passo?" | Executores | Líder do processo |
| Técnico | ESP | Especificação Técnica | "Com quais dados e regras de cálculo?" | Analistas, TI | Analista responsável |

Documentos de nível superior orientam e restringem os de nível inferior.

## Sistema de Codificação

Formato: `[TIPO]-[AREA]-[NNN]`

| Componente | Descrição | Valores Válidos |
|------------|-----------|-----------------|
| TIPO | Tipo de documento | `POL`, `MAN`, `INS`, `ESP` |
| AREA | Área ou processo | `M7` (holding), `PERF`, `INV`, `CRE`, `UNI`, `SEG` |
| NNN | Número sequencial (3 dígitos, zero-padded) | `001`, `002`, `003`... |

Exemplos:
- `POL-M7-001`: Política de Gestão por Processos
- `MAN-INV-001`: Manual de Operação do Funil Investimentos
- `INS-PERF-001`: Instrução de Fechamento Mensal de Performance
- `ESP-PERF-001`: Especificação de Cálculo de Indicadores

## Ciclo de Vida do Documento

| Etapa | Responsável | Descrição |
|-------|-------------|-----------|
| 1. Elaboração | Analista / Líder | Redigir conforme template padrão |
| 2. Revisão | Pares / Stakeholders | Revisar conteúdo, coerência, aplicabilidade |
| 3. Aprovação | Conforme hierarquia | Aprovação formal |
| 4. Publicação | Performance | Publicar no repositório oficial, comunicar |
| 5. Treinamento | Líder do Processo | Treinar equipe no novo padrão |
| 6. Verificação | Performance / Líder | Avaliar aderência |
| 7. Revisão periódica | Dono do documento | Atualizar conforme frequência definida |

## Frequências de Revisão

| Tipo | Frequência |
|------|------------|
| POL (Política) | Anual |
| MAN (Manual) | Semestral |
| INS (Instrução) | Trimestral |
| ESP (Especificação Técnica) | Trimestral |

## Quando Documentar é Obrigatório

- Novo processo implementado
- Processo existente remodelado
- Atividade com alto impacto em qualidade, segurança, custo ou compliance
- Dependência de conhecimento tácito em pessoas específicas
- Processos recorrentes (rituais, reuniões, rotinas) instituídos ou alterados

## Formatação Padrão

### Configuração de Página
- **Tamanho**: A4 (210mm x 297mm), orientação retrato
- **Margens**: Superior 3cm, Direita 2cm, Inferior 2cm, Esquerda 2,5cm

### Tipografia

| Elemento | Fonte | Tamanho | Peso | Cor |
|----------|-------|---------|------|-----|
| Corpo (Normal) | Arial | 11pt | Regular | #4F4E3C |
| Título 1 (seções) | Arial | 14pt | Negrito | #424135 |
| Título 2 (subseções) | Arial | 13pt | Negrito | #424135 |
| Título 3 (sub-subseções) | Arial | 11pt | Negrito | #424135 |
| Capa - Tipo | — | 26pt | Regular | #17365D |
| Capa - Subtítulo | — | 12pt | Regular | #4F81BD |

### Cores do Tema
- Primário escuro: #1F497D (navy)
- Primário claro: #EEECE1 (cinza quente/creme)
- Destaque 1: #4F81BD (azul aço)
- Destaque 2: #C0504D (vermelho sóbrio)

### Capa (todas as normativas)

Layout centralizado, nesta ordem:
1. Tipo do documento em MAIÚSCULAS (ex: "POLÍTICA", "MANUAL", "INSTRUÇÃO", "ESPECIFICAÇÃO TÉCNICA")
2. Código do documento (ex: `POL-[AREA]-[NNN]`)
3. Título do documento
4. "Holding M7"
5. "Versão X.X  |  DD/MM/AAAA"
6. Quebra de página

### Cabeçalho (todas as páginas após a capa)
```
[Título do Documento] | [Código] | v[Versão]
```

### Rodapé (todas as páginas após a capa)
```
Holding M7  ·  [Código]  ·  Página [N]
```

### Tabela de Controle do Documento

Imediatamente após a capa, usando estilo TableGrid com sombreamento alternado:
- **Linha cabeçalho**: fundo `#424135` (marrom escuro, texto branco)
- **Linhas pares**: fundo `#F5F3E8` (creme quente)
- **Linhas ímpares**: sem preenchimento (branco)

Campos obrigatórios:

| Campo | Descrição |
|-------|-----------|
| Código | Código do documento `[TIPO]-[AREA]-[NNN]` |
| Versão | Número da versão (ex: 1.0) |
| Tipo | Nome do tipo (Política, Manual, Instrução, Especificação Técnica) |
| Área | Área responsável |
| Data | Data no formato DD/MM/AAAA |
| Elaborado por | Nome do autor, cargo |
| Aprovado por | Nome do aprovador, cargo |
| Classificação | Sempre "Interno" |
| Revisão | Frequência de revisão |
| Documento superior | Código do documento pai (exceto POL-M7-001) |

### Tabela de Controle de Versões (final de todo documento)

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | DD/MM/AAAA | Autor | Versão inicial. |

### Numeração de Seções

- Título 1: `1.`, `2.`, `3.`...
- Título 2: `5.1`, `5.2`...
- Título 3: `5.1.1`, `5.4.1`...
- Listas usam formato bullet (não numerado)

## Regras de Referência Cruzada

- Todo documento referencia seu documento superior via campo "Documento superior"
- MAN lista INS e ESP relacionados em "Documentos Relacionados"
- INS lista MAN e ESP relacionados em "Referências"
- ESP lista dependências de sistema em "Dependências e Integrações"
- POL lista documentos relacionados em "Disposições Finais"
- **Sempre usar código do documento** para referências cruzadas (ex: `MAN-INV-001`), nunca texto livre

## Indicadores de Governança

| Indicador | Fórmula | Frequência | Meta |
|-----------|---------|------------|------|
| Cobertura documental | Processos documentados / Processos mapeados | Trimestral | >= 80% |
| Atualização de documentos | Dentro da validade / Total documentos | Trimestral | >= 90% |
| Aderência ao padrão | Conformes ao template / Total documentos | Semestral | 100% |

## Escalonamento de Exceções

| Tipo de Exceção | Aprovador |
|-----------------|-----------|
| Formato ou template do documento | Head de Área |
| Prazo ou cadência de revisão | Head de Área |
| Dispensa de documentação obrigatória | Diretoria |
| Alteração na hierarquia normativa | Diretoria |
