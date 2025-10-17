import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Visualizador de Dados Colados", layout="wide")

st.title("Visualizador de Dados Colados")

st.write("📋 Cole os dados da planilha abaixo (separados por tabulação):")

# Colunas que você quer manter
colunas_desejadas = [
    "Solicitação", "UGE", "Órgão", "Fornecedor", "CNPJ",
    "Licit SIASG", "Dt Solicitação", "Valor"
]

# Área de colagem expandida
dados_colados = st.text_area("Cole aqui os dados", height=700)

if dados_colados:
    try:
        # Lê os dados ignorando colunas extras
        df = pd.read_csv(
            io.StringIO(dados_colados),
            sep="\t",
            header=None,
            engine="python"
        )

        # Aplica nomes genéricos temporários
        df.columns = [f"col_{i}" for i in range(df.shape[1])]

        # Mapeia colunas desejadas com base na posição
        # Ajuste os índices conforme a estrutura real dos dados
        colunas_mapeadas = {
            "Solicitação": "col_0",
            "UGE": "col_3",
            "Órgão": "col_2",
            "Fornecedor": "col_9",
            "CNPJ": "col_10",
            "Licit SIASG": "col_11",
            "Dt Solicitação": "col_13",
            "Valor": "col_14"
        }

        df_filtrado = df[list(colunas_mapeadas.values())].copy()
        df_filtrado.columns = list(colunas_mapeadas.keys())

        # Conversão de valores
        df_filtrado["Valor"] = pd.to_numeric(
            df_filtrado["Valor"].astype(str).str.replace(".", "").str.replace(",", "."),
            errors="coerce"
        )

        # Conversão de datas
        df_filtrado["Dt Solicitação"] = pd.to_datetime(
            df_filtrado["Dt Solicitação"], dayfirst=True, errors="coerce"
        )

        st.subheader("📊 Tabela formatada:")
        st.dataframe(df_filtrado, use_container_width=True, height=600)

        # Botão para baixar como CSV
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar como CSV", csv, "dados_ajustados.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Erro ao processar os dados: {e}")
