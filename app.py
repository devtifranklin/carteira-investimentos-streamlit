import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor de Carteira", layout="wide")

st.title("Gestor de Carteira de Investimentos")

# Entrada do valor total
valor_total = st.number_input("Valor total disponível para investir (R$)", min_value=0.0, step=100.0)

# Cadastro dos ativos
st.subheader("Cadastro de Ativos")

with st.form("form_ativos"):
    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Nome do ativo (ex: Tesouro Selic, PETR4)")
    with col2:
        classe = st.selectbox("Classe do Ativo", ["Renda Fixa", "Multimercado", "Ações", "Exterior", "Cripto", "Outros"])
    with col3:
        percentual = st.number_input("Percentual da carteira (%)", min_value=0.0, max_value=100.0, step=0.5)

    adicionar = st.form_submit_button("Adicionar ativo")

# Inicializar a sessão de ativos
if "ativos" not in st.session_state:
    st.session_state["ativos"] = []

# Adicionar ativo à lista
if adicionar and nome and percentual > 0:
    st.session_state["ativos"].append({
        "Ativo": nome,
        "Classe": classe,
        "Percentual (%)": percentual
    })

# Mostrar ativos cadastrados
if st.session_state["ativos"]:
    st.subheader("Carteira Cadastrada")
    df = pd.DataFrame(st.session_state["ativos"])

    # Soma dos percentuais
    total_percentual = df["Percentual (%)"].sum()

    # Cálculo dos valores
    df["Valor Alocado (R$)"] = df["Percentual (%)"] / 100 * valor_total

    # Exibir mensagem de alerta
    if total_percentual < 100:
        st.warning(f"A soma dos percentuais é de {total_percentual:.2f}%. Adicione mais ativos ou ajuste os percentuais.")
    elif total_percentual > 100:
        st.error(f"A soma dos percentuais é de {total_percentual:.2f}%. Os percentuais ultrapassam 100%!")
    else:
        st.success("Carteira balanceada corretamente!")

    st.dataframe(df, use_container_width=True)

    # Gráficos
    st.subheader("Distribuição por Classe de Ativo")

    df_classe = df.groupby("Classe").sum(numeric_only=True).reset_index()
    st.bar_chart(data=df_classe, x="Classe", y="Valor Alocado (R$)")

    st.subheader("Distribuição por Ativo")
    st.bar_chart(data=df, x="Ativo", y="Valor Alocado (R$)")

    # Botão para limpar
    if st.button("Limpar Carteira"):
        st.session_state["ativos"] = []

else:
    st.info("Adicione ativos para começar a montar sua carteira.")
