import streamlit as st
import pandas as pd


# --- FUNÇÃO PARA INICIALIZAR O ESTADO ---
def inicializar_estado():
    if 'avaliacoes' not in st.session_state:
        st.session_state.avaliacoes = []


# --- CHAMADA DA FUNÇÃO DE INICIALIZAÇÃO ---
inicializar_estado()

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
    .st-emotion-cache-1avcm0n { /* Classe do st.metric */
        border: 1px solid #e1e1e1;
        border-radius: 10px;
        padding: 15px;
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
    demanda_input = st.text_area("Descrição da Demanda", placeholder="O que precisa ser feito?", key="demanda")
    justificativa = st.text_area("Justificativa e Recomendação", placeholder="Por que fazer isso agora?",
                                 key="justificativa")

with col_desc2:
    st.markdown("**🔍 Validação de Mercado**")
    comparativo = st.text_area("Comparativo com Mercado",
                               placeholder="Ex: O concorrente X já possui essa feature nativa.", key="comparativo")
    referencia = st.text_input("Referência / Link do Benchmarking", placeholder="https://...", key="referencia")
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
    # A EVOLUÇÃO QUE VOCÊ SUGERIU!
    esforco_label = st.select_slider(
        "Esforço Técnico",
        options=["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"],
        value="Médio",
        help="Estimativa do tempo/recursos. Inspirado em T-shirt Sizing (PP, P, M, G, GG)."
    )
    esforco_map = {"Muito Baixo": 1, "Baixo": 3, "Médio": 5, "Alto": 8, "Muito Alto": 13}
    val_esforco = esforco_map[esforco_label]

# --- CÁLCULO ---
score_base = (reach * impact * val_confianca) / val_esforco
score_final = score_base * fator_perfil * fator_churn

st.markdown("---")

if st.button("📊 AVALIAR E ADICIONAR À LISTA"):
    if not demanda_input:
        st.error("Por favor, preencha a 'Descrição da Demanda' antes de avaliar.")
    else:
        # st.balloons()
        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            st.subheader("⚖️ Veredito")
            if score_final >= 8:
                st.metric(label="Status da Demanda", value="CRÍTICA", delta=f"{score_final:.2f} Score")
                st.success("Mover para o topo do backlog imediatamente.")
            elif score_final >= 3:
                st.metric(label="Status da Demanda", value="VÁLIDA", delta=f"{score_final:.2f} Score",
                          delta_color="off")
                st.warning("Planejar para os próximos ciclos.")
            else:
                st.metric(label="Status da Demanda", value="BAIXA", delta=f"{score_final:.2f} Score",
                          delta_color="inverse")
                st.error("Considerar descarte ou reavaliação futura.")

        with res_col2:
            st.subheader("🧮 Memória de Cálculo")
            st.code(f"""
            (Alcance: {reach} * Impacto: {impact} * Confiança: {val_confianca}) / Esforço: {val_esforco} ({esforco_label})
            Score Base = {score_base:.2f}
            Multiplicador Perfil: x{fator_perfil} ({perfil_cliente})
            Multiplicador Churn: x{fator_churn}
            ---------------------------
            Score Final = {score_final:.2f}
            """)

        # Adicionar a avaliação ao histórico no st.session_state
        nova_avaliacao = {
            "Demanda": demanda_input,
            "Score Final": f"{score_final:.2f}",
            "Cliente": cliente_nome or "N/A",
            "Perfil": perfil_cliente,
            "Churn": "Sim" if ameaca_churn else "Não",
            "Alcance": reach,
            "Impacto": impact,
            "Confiança": confianca_label,
            "Esforço": esforco_label,
        }
        st.session_state.avaliacoes.append(nova_avaliacao)

# --- EXIBIÇÃO DO HISTÓRICO DE AVALIAÇÕES ---
if st.session_state.avaliacoes:
    st.markdown("---")
    st.header("📋 Histórico de Priorização")

    df_avaliacoes = pd.DataFrame(st.session_state.avaliacoes)

    # Ordenar por Score Final (convertendo para float antes)
    df_avaliacoes['Score Final'] = df_avaliacoes['Score Final'].astype(float)
    df_avaliacoes = df_avaliacoes.sort_values(by="Score Final", ascending=False).reset_index(drop=True)
    df_avaliacoes.index += 1  # Começar o índice em 1

    st.dataframe(df_avaliacoes, use_container_width=True)

    # Botão para limpar a lista
    if st.button("🗑️ Limpar Histórico"):
        st.session_state.avaliacoes = []
        st.rerun()