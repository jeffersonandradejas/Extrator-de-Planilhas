import streamlit as st
import pandas as pd
import io

st.title("Visualizador de Dados Colados")

st.write("Cole os dados da planilha abaixo (separados por tabulação):")

# Colunas originais
colunas = [
    "Solicitação", "UG", "Órgão", "UGE", "ND", "Item",
    "Situação", "Código", "Fornecedor", "CNPJ",
    "Licit SIASG", "Responsável", "Dt Solicitação", "Valor"
]

# Colunas a remover
colunas_remover = ["UG", "ND", "Item", "Código", "Responsável", "Situação"]

# Área de texto para colar os dados
dados_colados = st.text_area("Cole aqui os dados", height=400)

if dados_colados:
    try:
        # Converte o texto colado em DataFrame
        df = pd.read_csv(io.StringIO(dados_colados), sep="\t", header=None)
        df.columns = colunas[:df.shape[1]]

        # Remove colunas indesejadas (inclui Situação)
        df_filtrado = df.drop(columns=colunas_remover, errors="ignore")

        # Insere duas colunas em branco após "UGE"
        if "UGE" in df_filtrado.columns:
            idx_uge = df_filtrado.columns.get_loc("UGE") + 1
            df_filtrado.insert(idx_uge, "Coluna em branco 1", "")
            df_filtrado.insert(idx_uge + 1, "Coluna em branco 2", "")

        # Insere coluna em branco chamada "Situação" no lugar original
        if "Fornecedor" in df_filtrado.columns:
            idx_forn = df_filtrado.columns.get_loc("Fornecedor")
            df_filtrado.insert(idx_forn, "Situação", "")

        # Reordenar colunas: colocar "Valor" antes de "Dt Solicitação"
        cols = df_filtrado.columns.tolist()
        if "Valor" in cols and "Dt Solicitação" in cols:
            cols.remove("Valor")
            dt_index = cols.index("Dt Solicitação")
            cols.insert(dt_index, "Valor")
            df_filtrado = df_filtrado[cols]

        st.subheader("Tabela estruturada com ajustes:")
        st.dataframe(df_filtrado, use_container_width=True)

        # Botão para baixar como CSV
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar como CSV", csv, "dados_ajustados.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
