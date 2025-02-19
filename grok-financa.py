import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# =======================================================
# 1. CONFIGURAÇÃO INICIAL E LEITURA DE DADOS
# =======================================================
st.set_page_config(
    page_title="Relatório Financeiro STOCCO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
    <style>
    .header-style {color: #2A76BE; border-bottom: 3px solid #2A76BE;}
    .kpi-box {background: #f0f2f6; border-radius: 10px; padding: 20px; margin: 10px 0;}
    .metric-value {font-size: 26px !important; font-weight: 700 !important;}
    .dataframe {width: 100% !important;}
    </style>
    """, unsafe_allow_html=True)

# Função para ler dados
def carregar_dados():
    # Dados para Dezembro/24
    dados_dez24 = {
        'Cliente': ['COMESA S.L', 'CONSTRUCCIONES METALICAS', 'ISLAS GROUP', 'Materiart 14 S.L', 'PREST', 'TUBAL/STOCCO'],
        'Receita': [22387.50, 1525.00, 24975.00, 2800.00, 85412.50, 3624.00],
        'QteCol': [6, 1, 8, 1, 19, 1],
        'Qte_horas': [895.50, 61.00, 999.00, 112.00, 3416.50, 151.00],
        'Salarios': [12045.87, 667.75, 12965.79, 1457.12, 45994.36, 2042.12]
    }
    receitas_dez = pd.DataFrame(dados_dez24)
    receitas_dez['Mês'] = 'dez24'

    # Dados para Janeiro/25
    dados_jan25 = {
        'Cliente': ['ACASTILLAJE SYNERA S.L', 'COMESA S.L', 'CONSTRUCCIONES METALICAS', 'ISLAS GROUP', 'Materiart 14 S.L', 'SERRALHERIA MILLAN MARTINEZ', 'PREST', 'TUBAL/STOCCO'],
        'Receita': [5675.00, 35250.00, 13625.00, 8800.00, 4200.00, 1350.00, 99712.50, 4925.00],
        'QteCol': [1, 8, 5, 8, 1, 2, 18, 1],
        'Qte_horas': [227.00, 1410.00, 545.00, 352.00, 168.00, 54.00, 3988.50, 197.00],
        'Salarios': [3182.12, 18620.64, 7254.70, 4909.44, 2297.12, 719.02, 54270.01, 2732.12]
    }
    receitas_jan = pd.DataFrame(dados_jan25)
    receitas_jan['Mês'] = 'jan25'

    # Dados para Fevereiro/25
    dados_fev25 = {
        'Cliente': ['ACASTILLAJE SYNERA S.L', 'COMESA S.L', 'CONSTRUCCIONES METALICAS CONTINENTE S.L', 'MATERIAL ART 14 S.L', 'PREST INSTALACIONES Y MONTAJES S.L', 'SERRALHERIA MILLAN MARTINEZ', 'MONTAJES METALICOS FAYSOL', 'INDUSTRIAS GINOX SL', 'METALMECANICA DAVID SÁNCHEZ, S.L', 'INOXIDABLES DE MEDINA S.L'],
        'Receita': [11350.00, 13218.75, 8175.00, 4200.00, 99712.50, 1350.00, 12375.00, 1125.00, 3825.00, 4950.00],
        'QteCol': [2, 3, 3, 1, 18, 2, 11, 1, 1, 2],
        'Qte_horas': [454.00, 528.75, 327.00, 168.00, 3988.50, 54.00, 495.00, 45.00, 153.00, 198.00],
        'Salarios': [6810.00, 7931.25, 4905.00, 2520.00, 59827.50, 810.00, 7425.00, 675.00, 2295.00, 2970.00]
    }
    receitas_fev = pd.DataFrame(dados_fev25)
    receitas_fev['Mês'] = 'fev25'

    # Combinar dados de receitas
    df_receitas = pd.concat([receitas_dez, receitas_jan, receitas_fev])
    
    # Ler dados de Despesas
    df_despesas = pd.DataFrame({
        'Despesa': ['Alojamentos', 'Folha Trabalhadores', 'Folha Administrativo', 'Benefícios', 'Aluguel escritório', 'Energia', 'Imposto (Encargos Sociais)', 'Imposto (IVA/IR/C)', 'Uniformes', 'Coches', 'Contabilidade', 'Comissões', 'Internet', 'Serviços de TI', 'Software', 'Condomínio', 'Juros e encargos de financiamentos e empréstimos', 'Taxas bancárias e administrativas', 'Multas e penalidades financeiras', 'Seguros patrimoniais (bens, equipamentos)', 'Seguros de saúde e vida para colaboradores'],
        'dez24': [4500.00, 75173.01, 0, 0, 5000.00, 600.00, 0, 0, 0, 1000.00, 250.00, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'jan25': [6000.00, 93985.17, 0, 0, 5000.00, 600.00, 0, 5600.00, 0, 1000.00, 250.00, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'fev25': [6000.00, 76168.75, 0, 0, 5000.00, 600.00, 0, 0, 0, 1000.00, 250.00, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    })
    
    return df_receitas, df_despesas

df_receitas, df_despesas = carregar_dados()

# Coordenadas dos clientes
client_locations = {
    "COMESA S.L": (41.40, 2.16),
    "CONSTRUCCIONES METALICAS": (41.39, 2.15),
    "ISLAS GROUP": (41.42, 2.17),
    "Materiart 14 S.L": (41.45, 2.20),
    "PREST": (41.35, 2.12),
    "TUBAL/STOCCO": (41.48, 2.13),
    "ACASTILLAJE SYNERA S.L": (41.30, 2.10),
    "SERRALHERIA MILLAN MARTINEZ": (41.49, 2.18),
    "MONTAJES METALICOS FAYSOL": (41.31, 2.09),
    "INDUSTRIAS GINOX SL": (41.32, 2.11),
    "METALMECANICA DAVID SÁNCHEZ, S.L": (41.37, 2.19),
    "INOXIDABLES DE MEDINA S.L": (41.36, 2.22),
    "CONSTRUCCIONES METALICAS CONTINENTE S.L": (41.39, 2.15),
    "MATERIAL ART 14 S.L": (41.45, 2.20),
    "PREST INSTALACIONES Y MONTAJES S.L": (41.35, 2.12)
}

# Adicionar coordenadas
df_receitas['lat'] = df_receitas['Cliente'].apply(lambda x: client_locations.get(x, (41.38, 2.17))[0])
df_receitas['lon'] = df_receitas['Cliente'].apply(lambda x: client_locations.get(x, (41.38, 2.17))[1])

# =======================================================
# 3. INTERFACE DO USUÁRIO
# =======================================================
# Cabeçalho
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://i.imgur.com/nJYIiDz.png", width=150)
with col2:
    st.markdown("<h1 class='header-style'>RELATÓRIO FINANCEIRO - STOCCO</h1>", unsafe_allow_html=True)

# Filtros
periodo = st.selectbox("Selecione o período:", 
                      ["dez24", "jan25", "fev25", "Trimestre (dez24-jan25-fev25)"], 
                      index=3)

# Processar dados conforme filtro
if periodo == "Trimestre (dez24-jan25-fev25)":
    receitas_filtro = df_receitas
    despesas_filtro = df_despesas
else:
    receitas_filtro = df_receitas[df_receitas['Mês'] == periodo]
    despesas_filtro = df_despesas[['Despesa', periodo]]

# Calcular KPIs
total_receita = receitas_filtro['Receita'].sum()

if periodo == "Trimestre (dez24-jan25-fev25)":
    total_despesa = df_despesas[['dez24', 'jan25', 'fev25']].sum().sum()
else:
    total_despesa = df_despesas[periodo].sum()

lucro = total_receita - total_despesa
margem = (lucro / total_receita) * 100 if total_receita > 0 else 0

# Exibir KPIs
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='kpi-box'>💰 Receita Total<br><span class='metric-value'>€ {total_receita:,.2f}</span></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-box'>📉 Despesa Total<br><span class='metric-value'>€ {total_despesa:,.2f}</span></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-box'>📈 Lucro Líquido<br><span class='metric-value'>€ {lucro:,.2f}</span></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-box'>🎯 Margem<br><span class='metric-value'>{margem:.1f}%</span></div>", unsafe_allow_html=True)

# Gráficos e Visualizações
tab1, tab2, tab3 = st.tabs(["📈 Análise de Receitas", "📉 Análise de Despesas", "🌍 Mapa de Clientes"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Distribuição de Receitas")
        fig = px.pie(receitas_filtro, values='Receita', names='Cliente', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Relação Horas x Receita")
        # Corrigindo o erro de valores NaN na coluna 'QteCol'
        receitas_filtro['QteCol'] = receitas_filtro['QteCol'].fillna(0)
        fig = px.scatter(receitas_filtro, x='Qte_horas', y='Receita', 
                         size='QteCol', color='Cliente',
                         hover_name='Cliente', log_x=True)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Despesas por Categoria")
    if periodo == "Trimestre (dez24-jan25-fev25)":
        # Para o trimestre, somamos as despesas dos três meses
        despesas_filtro['Total'] = despesas_filtro['dez24'] + despesas_filtro['jan25'] + despesas_filtro['fev25']
        fig = px.bar(despesas_filtro, x='Despesa', y='Total', 
                     title=f'Despesas por Categoria - Trimestre (dez24-jan25-fev25)')
    else:
        fig = px.bar(despesas_filtro, x='Despesa', y=periodo, 
                     title=f'Despesas por Categoria - {periodo}')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Localização dos Clientes")
    # Criar um mapa base
    m = folium.Map(location=[41.38, 2.17], zoom_start=11)
    
    # Adicionar marcadores para cada cliente
    for _, row in receitas_filtro.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                      popup=f"{row['Cliente']}<br>Receita: € {row['Receita']:,.2f}<br>Horas: {row['Qte_horas']}<br>Colaboradores: {row['QteCol']}",
                      tooltip=row['Cliente']).add_to(m)
    
    # Exibir o mapa no Streamlit
    st_folium(m, width=700, height=400)

# Detalhes das Receitas
st.markdown("### Detalhes das Receitas")
st.dataframe(receitas_filtro.style.format({
    'Receita': '€ {:,.2f}'.format,
    'Qte_horas': '{:.2f}'.format,
    'Salarios': '€ {:,.2f}'.format
}))

# Detalhes das Despesas
st.markdown("### Detalhes das Despesas")
if periodo == "Trimestre (dez24-jan25-fev25)":
    st.dataframe(despesas_filtro.style.format({
        'dez24': '€ {:,.2f}'.format,
        'jan25': '€ {:,.2f}'.format,
        'fev25': '€ {:,.2f}'.format,
        'Total': '€ {:,.2f}'.format
    }))
else:
    st.dataframe(despesas_filtro.style.format({
        periodo: '€ {:,.2f}'.format
    }))

# Rodapé
st.markdown("---")
st.markdown("""
**Relatório Financeiro STOCCO**  
Diretoria Financeira | Versão 4.0 | Dados atualizados em 19/02/2025  
Contato: relatorios@stocco.com | Suporte técnico: ti@stocco.com
""")