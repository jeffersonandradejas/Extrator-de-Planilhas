import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Solicitação de Empenho - Visualizador", layout="wide")

st.title("Solicitação de Empenho - Visualizador")

# Cabeçalho com campo de colagem à esquerda e nome do desenvolvedor à direita
col1, col2 = st.columns([4, 1])
with col1:
    st.write("📋 Cole os dados da planilha abaixo (separados por tabulação):")
with col2:
    st.markdown("<div style='text-align: right; font-size: 14px;'>Desenvolvedor: <b>2S SAD Andrade</b></div>", unsafe_allow_html=True)

# Área de colagem
dados_colados = st.text_area("Cole aqui os dados", height=700)

if dados_colados:
    try:
        # Remove espaços em branco no início das linhas
        linhas = [linha.lstrip() for linha in dados_colados.strip().split("\n")]
        dados_limpos = "\n".join(linhas)

        # Lê os dados colados
        df = pd.read_csv(io.StringIO(dados_limpos), sep="\t", header=None, engine="python", on_bad_lines="skip")
        df.columns = [f"col_{i}" for i in range(df.shape[1])]

        # Mapeamento atualizado
        colunas_mapeadas = {
            "SOL": "col_0",
            "APOIADA": "col_2",     # UG Cred (HARF)
            "IL": "col_4",          # Códigos como C25117
            "FORNECEDOR": "col_9",
            "PAG": "col_10",
            "PREGÃO": "col_11",
            "VALOR": "col_14",
            "DATA": "col_13"
        }

        # Extrai colunas existentes
        colunas_existentes = [v for v in colunas_mapeadas.values() if v in df.columns]
        df_filtrado = df[colunas_existentes].copy()
        df_filtrado.columns = [k for k, v in colunas_mapeadas.items() if v in df.columns]

        # Insere colunas em branco após IL
        for i, nova_coluna in enumerate(["EMPENHO", "ID", "STATUS"]):
            df_filtrado.insert(3 + i, nova_coluna, "")

        # Formata VALOR
        if "VALOR" in df_filtrado.columns:
            df_filtrado["VALOR"] = df_filtrado["VALOR"].astype(str).str.replace(".", "").str.replace(",", ".")
            df_filtrado["VALOR"] = pd.to_numeric(df_filtrado["VALOR"], errors="coerce")
            df_filtrado["VALOR"] = df_filtrado["VALOR"].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else "")

        # Formata DATA
        if "DATA" in df_filtrado.columns:
            df_filtrado["DATA"] = pd.to_datetime(df_filtrado["DATA"], dayfirst=True, errors="coerce")
            df_filtrado["DATA"] = df_filtrado["DATA"].dt.strftime("%d/%m/%Y")

        # Reordena para colocar VALOR antes de DATA
        colunas_ordenadas = df_filtrado.columns.tolist()
        if "VALOR" in colunas_ordenadas and "DATA" in colunas_ordenadas:
            colunas_ordenadas.remove("VALOR")
            idx_data = colunas_ordenadas.index("DATA")
            colunas_ordenadas.insert(idx_data, "VALOR")
            df_filtrado = df_filtrado[colunas_ordenadas]

        st.subheader("📊 Tabela formatada:")
        st.dataframe(df_filtrado, use_container_width=True, height=600)

        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar como CSV", csv, "dados_formatados.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Erro ao processar os dados: {e}")
