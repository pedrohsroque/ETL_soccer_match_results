import pandas as pd
import streamlit as st
import os, sys
sys.path.append(os.getcwd())
from transformers.pandas.transformer import transform_data

st.set_page_config(page_title="Tabela", page_icon="", layout="wide")
sidebar = st.sidebar
year = sidebar.selectbox(
    "Ano",
    options=[
        "2023",
        "2022",
    ],
)
competition = sidebar.selectbox(
    "Competição",
    options=[
        "Brasileiro Série A",
        "Brasileiro Série B",
    ],
)
st.title(f"Classificação - Campeonato {competition} {year}")
data = pd.read_csv(f"data/Campeonato {competition} {year}.csv")
turno = sidebar.radio(
    "Turno",
    options=[
        "Ambos",
        "1º turno",
        "2º turno",
    ],
)
data["Turno"] = data["round"].apply(lambda x: "1" if int(x[1:-1]) < 20 else "2")
if turno != "Ambos":
    data = data[data["Turno"] == turno[0]]
data = data.drop(["Turno"], axis="columns")
data = transform_data(data)


def color_rank(data):
    color = "#BBBBBB"
    if data["team"] in ["Fluminense", "São Paulo"]:
        color = "#2b84bf"
    elif data["rank"] <= 4:
        color = "#2b84bf"
    elif data["rank"] <= 6:
        color = "#55bbff"
    elif data["rank"] <= 14:
        color = "#009900"
    elif data["rank"] >= 17:
        color = "#FF6666"
    return [f"background-color: {color}"] * 1 + ["background-color: white"] * 10


st.dataframe(
    data.style.apply(color_rank, axis="columns"), hide_index=True, height=738, width=850
)
