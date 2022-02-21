import streamlit as st
import agenda, submit
import pytz
from datetime import datetime

tz_brasil = pytz.timezone("America/Sao_Paulo")

st.image("Even-logo.png")
st.write("Um quadro de notas comunitário & horários de aula rápido e prático.✅")
st.caption(f"Última atualização: {datetime.now(tz_brasil).strftime('%H:%M')}")

#selecionar página
pag = st.sidebar.radio("Selecione sua Página:", ["Ver agenda", "Criar nova agenda"])

if pag == "Ver agenda":
    agenda.render()
elif pag == "Criar nova agenda":
    submit.render()
