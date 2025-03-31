import streamlit as st
import pandas as pd
import base64
import requests
from datetime import datetime

# Configurações do seu GitHub
GITHUB_TOKEN = "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                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               "
REPO_OWNER = "pfalcaopy"
REPO_NAME = "test"
BRANCH = "main"  # ou 'master'
SAVE_PATH = "data"  # pasta no repo

# Headers para autenticação
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

st.title("Upload e envio de CSV para GitHub")

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    file_content = uploaded_file.getvalue()
    file_base64 = base64.b64encode(file_content).decode()

    # Nome do arquivo com timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = uploaded_file.name.replace(".csv", f"_{now}.csv")
    path_in_repo = f"{SAVE_PATH}/{filename}"

    # Endpoint da API
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path_in_repo}"

    # Dados para envio
    data = {
        "message": f"Adiciona CSV {filename} via Streamlit",
        "content": file_base64,
        "branch": BRANCH
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        st.success(f"✅ Arquivo enviado com sucesso para o GitHub: {path_in_repo}")
        st.markdown(f"[🔗 Ver no GitHub](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/{path_in_repo})")
    else:
        st.error("❌ Erro ao enviar arquivo para o GitHub")
        st.text(response.json())
