import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.markdown("""
<style>
    /* Fundo da página */
    .stApp {
        background-color: #F3F6FA;
    }

    /* Margens e largura do conteúdo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    /* Margens menores em telas estreitas */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    /* Títulos */
    h1, h2, h3 {
        color: #142B4A;
    }

    /* Cartões dos indicadores */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E8F0;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(20, 43, 74, 0.05);
    }

    /* Caixa de explicações */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    /* Avisos */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Linhas divisórias */
    hr {
        border-color: #DCE5EF;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# INTRODUÇÃO
# =====================================================

st.title("📊 B3 S.A. - Desenvolvimento de Mercado")

st.markdown("""
### Introdução

A B3 S.A. – Brasil, Bolsa, Balcão é a bolsa de valores do Brasil e desempenha um papel importante
na infraestrutura do mercado financeiro e de capitais.

Este dashboard analisa a evolução do mercado entre **2020 e 2025**,
considerando o número de investidores pessoa física em renda variável,
o valor em custódia e as emissões públicas de títulos de dívida
corporativa.

O objetivo é compreender como esses indicadores evoluíram ao longo
do período e discutir sua relação com o financiamento das empresas,
o desenvolvimento econômico e os Objetivos de Desenvolvimento
Sustentável (ODS).

**Período analisado:** 2020 a 2025.
""")

st.info(
    "Os indicadores de investidores e custódia representam a posição "
    "no encerramento de cada ano. Emissões representam o volume emitido "
    "ao longo do ano. Por isso, são indicadores diferentes."
)

# =====================================================
# 1. DADOS
# =====================================================

# Investidores em renda variável e posição em custódia
# Valores em milhões de CPFs e R$ bilhões.
#
# Emissões corporativas:
# os valores de 2023 a 2025 seguem a série publicada pela B3.
# 2020 a 2022 ficam sem valor para não misturar séries
# de definições diferentes.

dados = pd.DataFrame({
    "Ano": [2020, 2021, 2022, 2023, 2024, 2025],

    "Investidores_milhoes": [
        2.7, 4.2, 5.0, 5.0, 5.3, 5.5
    ],

    "Custodia_bilhoes": [
        457.1, 500.1, 459.5, 550.8, 528.3, 636.2
    ],

    "Emissoes_bilhoes": [
        None, None, None, 345.4, 608.1, 647.5
    ]
})


# =====================================================
# GUIA DE TERMOS E INDICADORES
# =====================================================

with st.expander("📖 Entenda os indicadores e termos do painel"):

    st.markdown("""
    **B3 — Bolsa do Brasil:**  
    Empresa que oferece infraestrutura para negociação e registro
    de ativos financeiros no mercado brasileiro.

    **Investidores em renda variável:**  
    Pessoas físicas que investem em ativos cujo retorno pode variar,
    como ações e fundos imobiliários.

    **Valor em custódia:**  
    Valor dos ativos mantidos pelos investidores na B3S.A. em uma
    determinada data. Não representa dinheiro disponível em conta.

    **Emissões de dívida corporativa:**  
    Recursos captados por empresas ao emitir títulos de dívida
    no mercado de capitais.

    **Debêntures:**  
    Títulos de dívida emitidos por empresas para captar recursos
    de investidores.

    **CRI — Certificado de Recebíveis Imobiliários:**  
    Título de renda fixa lastreado em créditos do setor imobiliário.

    **CRA — Certificado de Recebíveis do Agronegócio:**  
    Título de renda fixa lastreado em créditos ligados ao agronegócio.

    **Notas comerciais:**  
    Títulos de dívida que empresas podem emitir para captar recursos,
    geralmente utilizados em financiamentos de curto ou médio prazo.

    **ODS — Objetivos de Desenvolvimento Sustentável:**  
    Conjunto de objetivos da ONU voltados a desafios econômicos,
    sociais e ambientais.
    """)


# =====================================================
# 2. INDICADORES PRINCIPAIS
# =====================================================

inicio = dados.iloc[0]
fim = dados.iloc[-1]

crescimento_investidores = (
    fim["Investidores_milhoes"] /
    inicio["Investidores_milhoes"] - 1
) * 100

crescimento_custodia = (
    fim["Custodia_bilhoes"] /
    inicio["Custodia_bilhoes"] - 1
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Investidores em 2025",
    f'{fim["Investidores_milhoes"]:.1f} milhões',
    f"{crescimento_investidores:+.1f}% desde 2020"
)

col2.metric(
    "Custódia em 2025",
    f'R$ {fim["Custodia_bilhoes"]:.1f} bi',
    f"{crescimento_custodia:+.1f}% desde 2020"
)

col3.metric(
    "Emissões em 2025",
    f'R$ {fim["Emissoes_bilhoes"]:.1f} bi',
    "+6,5% contra 2024"
)

col4.metric(
    "Período analisado",
    "2020–2025",
    "6 anos"
)

st.caption(
    "Fonte: B3. Indicadores de pessoas físicas em renda variável "
    "e emissões públicas de dívida corporativa."
)

st.divider()

# =====================================================
# 3. EVOLUÇÃO DOS INVESTIDORES
# =====================================================

st.header("📈 Evolução dos investidores")

st.markdown("""
O número de investidores ajuda a observar a participação das pessoas
físicas no mercado de renda variável ao longo do tempo.
""")

fig_investidores = px.line(
    dados,
    x="Ano",
    y="Investidores_milhoes",
    markers=True,
    text="Investidores_milhoes",
    labels={
        "Ano": "Ano",
        "Investidores_milhoes": "Investidores (milhões)"
    }
)

fig_investidores.update_traces(
    texttemplate="%{text:.1f}",
    textposition="top center",
    line=dict(width=3),
    marker=dict(size=8)
)

fig_investidores.update_layout(
    height=420,
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="Milhões de investidores",
    showlegend=False
)

st.plotly_chart(
    fig_investidores,
    use_container_width=True
)

st.caption(
    "Observação: número de investidores registrados em renda variável "
    "no encerramento de cada ano."
)

# =====================================================
# 4. VALOR EM CUSTÓDIA
# =====================================================

st.divider()
st.header("🏛️ Evolução do valor em custódia")

st.markdown("""
O valor em custódia representa o valor dos ativos mantidos pelos
investidores. A evolução desse indicador pode refletir mudanças nos
preços dos ativos e nas posições dos investidores.
""")

fig_custodia = px.bar(
    dados,
    x="Ano",
    y="Custodia_bilhoes",
    text="Custodia_bilhoes",
    labels={
        "Ano": "Ano",
        "Custodia_bilhoes": "Custódia (R$ bilhões)"
    }
)

fig_custodia.update_traces(
    texttemplate="R$ %{text:.1f} bi",
    textposition="outside"
)

fig_custodia.update_layout(
    height=440,
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="R$ bilhões",
    showlegend=False
)

st.plotly_chart(
    fig_custodia,
    use_container_width=True
)

st.caption(
    "A custódia é uma posição de fim de ano, não um fluxo anual. "
)

# =====================================================
# 5. EMISSÕES CORPORATIVAS
# =====================================================

st.divider()
st.header("🏢 Emissões de dívida corporativa")

st.markdown("""
As empresas podem emitir títulos de dívida para captar recursos
por meio do mercado de capitais. Esse indicador mostra o volume
anual de emissões públicas divulgado pela B3.
""")

emissoes = dados.dropna(
    subset=["Emissoes_bilhoes"]
).copy()

fig_emissoes = px.bar(
    emissoes,
    x="Ano",
    y="Emissoes_bilhoes",
    text="Emissoes_bilhoes",
    labels={
        "Ano": "Ano",
        "Emissoes_bilhoes": "Emissões (R$ bilhões)"
    }
)

fig_emissoes.update_traces(
    texttemplate="R$ %{text:.1f} bi",
    textposition="outside"
)

fig_emissoes.update_layout(
    height=440,
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    yaxis_title="R$ bilhões",
    showlegend=False
)

st.plotly_chart(
    fig_emissoes,
    use_container_width=True
)

st.warning(
    "Fonte: B3. As emissões de dívida corporativa são apresentadas "
    "para o período de 2023 a 2025."
)

# =====================================================
# 6. COMPOSIÇÃO DAS EMISSÕES
# =====================================================

st.divider()
st.header("📑 Composição por instrumento financeiro")

st.markdown("""
Este gráfico compara os principais instrumentos utilizados nas
emissões públicas de dívida corporativa em 2024 e 2025.
""")

composicao = pd.DataFrame({
    "Ano": [
        2024, 2024, 2024, 2024,
        2025, 2025, 2025, 2025
    ],
    "Instrumento": [
        "Debêntures",
        "CRI",
        "CRA",
        "Notas comerciais",
        "Debêntures",
        "CRI",
        "CRA",
        "Notas comerciais"
    ],
    "Valor_bilhoes": [
        465.8, 57.5, 40.8, 44.0,
        496.3, 50.8, 46.0, 54.0
    ]
})

fig_composicao = px.bar(
    composicao,
    x="Instrumento",
    y="Valor_bilhoes",
    color="Ano",
    barmode="group",
    text="Valor_bilhoes",
    labels={
        "Instrumento": "Instrumento financeiro",
        "Valor_bilhoes": "Valor (R$ bilhões)",
        "Ano": "Ano"
    }
)

fig_composicao.update_traces(
    texttemplate="R$ %{text:.1f}",
    textposition="outside"
)

fig_composicao.update_layout(
    height=480,
    yaxis_title="R$ bilhões",
    legend_title="Ano"
)

st.plotly_chart(
    fig_composicao,
    use_container_width=True
)

st.caption(
    "Fonte: B3. Valores publicados para cada instrumento. "
    "Os valores por categoria podem não totalizar exatamente o "
    "total anual divulgado devido a arredondamentos ou diferenças "
    "de apresentação; consulte os relatórios oficiais."
)

# =====================================================
# 7. TABELA HISTÓRICA
# =====================================================

st.divider()
st.header("🔍 Tabela geral — 2020 a 2025")

st.markdown("""
A tabela permite consultar os indicadores anuais em um único lugar.
""")

tabela = dados.rename(columns={
    "Ano": "Ano",
    "Investidores_milhoes": "Investidores (milhões)",
    "Custodia_bilhoes": "Custódia (R$ bilhões)",
    "Emissoes_bilhoes": "Emissões corporativas (R$ bilhões)"
})

st.dataframe(
    tabela,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# 8. IMPACTO ECONÔMICO E ODS
# =====================================================

st.divider()
st.header("🌍 Impacto econômico e relação com os ODS")

st.subheader(" 📈 ODS 8 — Trabalho decente e crescimento econômico")

st.markdown("""
O mercado de capitais pode oferecer às empresas alternativas
para captar recursos e financiar suas atividades. A evolução das
emissões corporativas ajuda a analisar a importância desse canal
de financiamento para a economia.
""")

st.subheader(" 🏗️ ODS 9 — Indústria, inovação e infraestrutura")

st.markdown("""
Os recursos captados no mercado de capitais podem financiar projetos
empresariais, infraestrutura e inovação. Para comprovar resultados
específicos, é necessário analisar dados sobre a destinação dos
recursos e os projetos financiados.
""")

st.subheader("🌱 Sustentabilidade e outras ODS")

st.markdown("""
A atuação da B3 vai além do mercado financeiro. A companhia também
desenvolve iniciativas ambientais, sociais e de governança (ASG),
contribuindo para a promoção de práticas mais sustentáveis.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌳 Meio ambiente")
    st.write(
        "Iniciativas relacionadas à gestão de emissões, "
        "mudanças climáticas e índices como o ICO2 B3."
    )

with col2:
    st.markdown("### 🤝 Responsabilidade social")
    st.write(
        "A B3 Social apoia iniciativas sociais, incluindo "
        "projetos relacionados à educação e à redução "
        "das desigualdades."
    )

with col3:
    st.markdown("### 🏢 Governança")
    st.write(
        "A B3 incentiva a transparência, a divulgação de "
        "informações ASG e as boas práticas empresariais."
    )

st.markdown("""
Além das ODS 8 e 9, que são o foco deste trabalho, a atuação da
B3 também se relaciona a outros Objetivos de Desenvolvimento
Sustentável da ONU.

Essas iniciativas ampliam a compreensão do papel da companhia
no desenvolvimento sustentável, embora não sejam medidas
diretamente por todos os indicadores financeiros apresentados
neste dashboard.
""")

# =====================================================
# 9. CONCLUSÃO
# =====================================================

st.divider()
st.header(" 🎯 Conclusão")

st.markdown("""
Entre 2020 e 2025, a base de investidores pessoa física em renda
variável e o valor em custódia apresentaram crescimento no período,
embora com oscilações entre os anos.

As emissões públicas de dívida corporativa também cresceram
entre 2023 e 2025, atingindo um recorde em 2025 segundo a B3.

Em conjunto, esses indicadores ajudam a compreender a evolução
do mercado de capitais e sua função como alternativa de financiamento
para empresas.
""")

