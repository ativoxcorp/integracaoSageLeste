import pandas as pd
import numpy as np
import streamlit as st
from st_aggrid import JsCode, AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

import src.pages.atualizarProdutos as atualizarProdutos
import src.pages.gerarNotasai as gerarNotasai

st.set_page_config(page_title="Integração Sage", page_icon="🐞", layout="centered")


st.sidebar.title("Menu")
add_selectbox = st.sidebar.selectbox(
    "Escolha uma operação",
    ("Atualizar Produtos", "Gerar notasai")
)

if add_selectbox == 'Atualizar Produtos':
  atualizarProdutos.atualizarProdutos()

if add_selectbox == 'Gerar notasai':
  gerarNotasai.gerarNotasai()

