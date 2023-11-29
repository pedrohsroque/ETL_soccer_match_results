import streamlit as st
import os, sys
sys.path.append(os.getcwd())
from extractors.requests_extractor import RequestsExtractor
from dotenv import load_dotenv

load_dotenv()

if 'updating_data' not in st.session_state:
    st.session_state.updating_data = False

def is_data_incomplete(filename: str) -> bool:
    with open(f"data/{filename}.csv", "r", encoding='utf-8') as f:
        return any(['None x None' in linha for linha in f.readlines()])

championships_list = []

refresh_serie_a = st.button("Atualizar Série A 2023")
refresh_serie_b = st.button("Atualizar Série B 2023")
refresh_password = st.text_input("Senha para atualizar:", type="password")
refresh_condition = refresh_password == os.getenv("refresh_password")

if not st.session_state.updating_data and refresh_condition:
    print("Aqui")
    if refresh_serie_a:
        championship_name = "Campeonato Brasileiro Série A 2023"
        if is_data_incomplete(championship_name):
            championships_list.append(championship_name)

    if refresh_serie_b:
        championship_name = "Campeonato Brasileiro Série B 2023"
        if is_data_incomplete(championship_name):
            championships_list.append(championship_name)

if len(championships_list) > 0:
    st.session_state.updating_data = True
    st.write("Atualizando dados")
    extractor = RequestsExtractor()
    for championship in championships_list:
        print(championship)
        championship_data = extractor.get_championship_data(championship)
        extractor.save_data(championship_data, championship)
    st.write("Dados Atualizados")
    st.session_state.updating_data = False
