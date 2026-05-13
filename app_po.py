import streamlit as st
import pandas as pd

# Configuração da Interface
st.set_page_config(page_title="Product Discovery - Portal de Atendimento", layout="wide")

st.title("🚀 Priorização Estratégica (Lógica RICE Refinada)")
st.subheader("Framework de Decisão Baseado em Valor, Confiança e Esforço")
st.markdown("---")

# --- PAINEL LATERAL: CONTEXTO E MULTIPLICADORES ---
st.sidebar.header("📍 Contexto Estratégico")
cliente_nome = st.sidebar.text_input("Nome do Cliente/Solicitante")

perfil_cliente = st.sidebar.selectbox(
    "Perfil do Cliente",
    ["Padrão", "Em Crescimento", "Estratégico (Key Account)"],
    index=0
)

ameaca_churn = st.sidebar.checkbox("🚨 Risco de Churn? (Ameaça de saída)")

# Mapeamento de Multiplicadores Estratégicos (Evita distorção por soma)
mult_perfil = {"Padrão": 1.0, "Em Crescimento": 1.2, "Estratégico (Key Account)": 1.5}
fator_perfil = mult_perfil[perfil_cliente]
fator_churn = 1.8 if ameaca_churn else 1.0

# --- ÁREA PRINCIPAL: ENTRADA DE DADOS ---
st.header("1. Detalhamento da Oportunidade")
col_desc1, col_desc2 = st.columns(2)

with col_desc1:
    raw_input = st.text_area("Descrição da Demanda", placeholder="O que precisa ser feito?")
    justificativa = st.text_area("Justificativa e Recomendação", placeholder="Por que fazer isso agora?")

with col_desc2:
    comparativo = st.text_area("Comparativo com Mercado", placeholder="Como os concorrentes resolvem isso?")
    referencia = st.text_input("Referência / Link do Benchmarking")

st.header("2. Métricas do Score (Fórmula RICE)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    escalabilidade = st.slider("Escalabilidade", 1, 10, 5, help="1: Customização isolada | 10: Atende toda a base.")
with col2:
    alinhamento = st.slider("Alinhamento", 1, 10, 5, help="O quanto segue o Roadmap Estratégico.")
with col3:
    reducao_esforco = st.slider("Impacto (Redução de Esforço)", 1, 10, 5, help="O quanto facilita a vida do usuário.")
with col4:
    confianca_label = st.select_slider("Confiança", options=["Baixa", "Média", "Alta"], value="Média")
    # Conversão para métrica numérica conforme solicitado
    confianca_map = {"Baixa": 0.5, "Média": 0.8, "Alta": 1.0}
    confianca = confianca_map[confianca_label]

st.markdown("---")
st.header("3. Complexidade e Esforço")
col_e1, col_e2 = st.columns([2, 1])

with col_e1:
    complexidade_label = st.select_slider(
        "Complexidade de Implementação (Esforço Técnico)",
        options=["Baixa", "Média", "Alta"],
        value="Média"
    )
    # Conversão para escala numérica (Denominador)
    esforco_map = {"Baixa": 1, "Média": 5, "Alta": 10}
    esforco_tecnico = esforco_map[complexidade_label]

with col_e2:
    st.info(f"**Peso do Esforço:** {esforco_tecnico}\n\n*(Quanto maior o esforço, menor será o score final)*")

# --- LÓGICA DE CÁLCULO REVISADA ---
# Fórmula: (E * A * R * C) / Esforço
numerador = (escalabilidade * alinhamento * reducao_esforco * confianca)
score_base = numerador / esforco_tecnico

# Aplicação dos multiplicadores estratégicos (Ajuste Final)
score_final = score_base * fator_perfil * fator_churn

# --- RESULTADO E VEREDITO ---
if st.button("📊 AVALIAR OPORTUNIDADE"):
    st.divider()

    col_veredito, col_detalhe = st.columns([1, 1])

    with col_veredito:
        st.subheader("⚖️ Veredito do Produto")

        # Thresholds baseados na nova escala multiplicativa
        if score_final >= 50:
            st.success(
                f"**PRIORIDADE CRÍTICA (Score: {score_final:.1f})**\n\nAlto valor com esforço viável. Mover para refinamento imediato.")
        elif score_final >= 20:
            st.warning(
                f"**OPORTUNIDADE VÁLIDA (Score: {score_final:.1f})**\n\nEquilíbrio positivo entre valor e esforço. Planejar conforme capacidade.")
        else:
            st.error(
                f"**BAIXA PRIORIDADE (Score: {score_final:.1f})**\n\nO custo técnico ou a falta de confiança superam os benefícios atuais.")

    with col_detalhe:
        st.subheader("🧮 Memória de Cálculo")
        st.markdown(f"""
        **Fórmula:** `(Escal. * Alinh. * Impacto * Conf.) / Esforço`

        *   **Valor Bruto:** {numerador:.1f}
        *   **Penalidade Esforço:** ÷ {esforco_tecnico}
        *   **Bônus Estratégico (Perfil):** x {fator_perfil}
        *   **Bônus Urgência (Churn):** x {fator_churn}
        ---
        **Score Final:** {score_final:.2f}
        """)

    # Tabela Resumo para Relatórios
    st.markdown("### 📋 Resumo para Registro")
    df_resumo = pd.DataFrame({
        "Critério": ["Cliente", "Confiança", "Esforço Técnico", "Impacto de Negócio", "Score Final"],
        "Valor": [cliente_nome, f"{confianca_label} ({confianca})", complexidade_label, f"{reducao_esforco}/10",
                  f"{score_final:.2f}"]
    })
    st.table(df_resumo)

    # Exibição de recomendações baseada no Modelo Kano simplificado (opcional)
    st.write(f"**Recomendação Técnica:** {justificativa}")