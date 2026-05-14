import streamlit as st
import pandas as pd

# Configuração da Interface
st.set_page_config(page_title="RICE Priority Pro", layout="wide", page_icon="🚀")

# Estilização básica via Markdown para melhorar o visual
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Priorização Estratégica (Lógica RICE)")
st.subheader("Framework de Decisão Baseado em Valor, Confiança e Esforço")
st.markdown("---")

# --- PAINEL LATERAL: CONTEXTO ---
with st.sidebar:
    st.header("📍 Contexto Estratégico")
    cliente_nome = st.text_input("Nome do Cliente/Solicitante")
    perfil_cliente = st.selectbox(
        "Perfil do Cliente",
        ["Padrão", "Em Crescimento", "Estratégico (Key Account)"],
        index=0
    )
    ameaca_churn = st.checkbox("🚨 Risco de Churn? (Ameaça de saída)")

    st.info("""
    **Dica:** O risco de churn atua como um acelerador de urgência, 
    multiplicando o valor final do score.
    """)

# Mapeamento de Multiplicadores
mult_perfil = {"Padrão": 1.0, "Em Crescimento": 1.2, "Estratégico (Key Account)": 1.5}
fator_perfil = mult_perfil[perfil_cliente]
fator_churn = 1.8 if ameaca_churn else 1.0

# --- ÁREA PRINCIPAL ---
st.header("1. Detalhamento da Oportunidade")
col_desc1, col_desc2 = st.columns(2)

with col_desc1:
    raw_input = st.text_area("Descrição da Demanda", placeholder="O que precisa ser feito?")
    justificativa = st.text_area("Justificativa e Recomendação", placeholder="Por que fazer isso agora?")

with col_desc2:
    st.markdown("**🔍 Validação de Mercado**")
    comparativo = st.text_area("Comparativo com Mercado",
                               placeholder="Ex: O concorrente X já possui essa feature nativa.")
    referencia = st.text_input("Referência / Link do Benchmarking", placeholder="https://...")
    st.caption("Use esta seção para embasar sua nota de 'Confiança' abaixo.")

st.markdown("---")
st.header("2. Métricas do Score (Fórmula RICE)")
c1, c2, c3, c4 = st.columns(4)

with c1:
    reach = st.slider("Alcance (Escalabilidade)", 1, 10, 5, help="1: Isolado | 10: Toda a base")
with c2:
    impact = st.slider("Impacto (Alinhamento)", 1, 10, 5, help="O quanto isso move o ponteiro do Roadmap")
with c3:
    confianca_label = st.select_slider("Confiança", options=["Baixa", "Média", "Alta"], value="Média")
    confianca_map = {"Baixa": 0.5, "Média": 0.8, "Alta": 1.0}
    val_confianca = confianca_map[confianca_label]
with c4:
    esforco_label = st.select_slider("Esforço Técnico", options=["Baixa", "Média", "Alta"], value="Média")
    esforco_map = {"Baixa": 1, "Média": 5, "Alta": 10}
    val_esforco = esforco_map[esforco_label]

# --- CÁLCULO ---
# RICE = (Reach * Impact * Confidence) / Effort
score_base = (reach * impact * val_confianca) / val_esforco
score_final = score_base * fator_perfil * fator_churn

st.markdown("---")

if st.button("📊 AVALIAR OPORTUNIDADE"):
    #st.balloons()

    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        st.subheader("⚖️ Veredito")
        if score_final >= 50:
            st.success(
                f"### PRIORIDADE CRÍTICA\n**Score: {score_final:.2f}**\n\nMover para o topo do backlog imediatamente.")
        elif score_final >= 20:
            st.warning(f"### OPORTUNIDADE VÁLIDA\n**Score: {score_final:.2f}**\n\nPlanejar para os próximos ciclos.")
        else:
            st.error(f"### BAIXA PRIORIDADE\n**Score: {score_final:.2f}**\n\nCusto técnico maior que o valor gerado.")

    with res_col2:
        st.subheader("🧮 Memória de Cálculo")
        st.code(f"""
        (Alcance: {reach} * Impacto: {impact} * Confiança: {val_confianca}) / Esforço: {val_esforco}
        Score Base = {score_base:.2f}
        Multiplicador Perfil: x{fator_perfil}
        Multiplicador Churn: x{fator_churn}
        ---------------------------
        Score Final = {score_final:.2f}
        """)

    # Tabela Resumo
    st.markdown("### 📋 Resumo para Registro")
    resumo_data = {
        "Atributo": ["Cliente", "Perfil", "Risco Churn", "Confiança", "Score Final"],
        "Valor": [cliente_nome or "Não informado", perfil_cliente, "Sim" if ameaca_churn else "Não", confianca_label,
                  f"{score_final:.2f}"]
    }
    st.table(pd.DataFrame(resumo_data))