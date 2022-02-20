import streamlit as st
import agenda, submit
from datetime import datetime

st.image("Even-logo.png")
st.write("Um quadro de notas comunitário & horários de aula rápido e prático.✅")
st.caption(f"Última atualização: {datetime.now().strftime('%H:%M')}")

#selecionar página
pag = st.sidebar.radio("Selecione sua Página:", ["Ver agenda", "Criar nova agenda"])

if pag == "Ver agenda":
    agenda.render()
elif pag == "Criar nova agenda":
    submit.render()