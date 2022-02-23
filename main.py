import streamlit as st
import agenda, submit
import pytz
from datetime import datetime

tz_brasil = pytz.timezone("America/Sao_Paulo")

# configurações da página
st.set_page_config(page_title= 'Even', 
                   page_icon="⌚",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       "About": """Esse App foi desenvolvido por [@LfLaguardia](https://github.com/lfzinho).
                        Sinta-se livre para requisitar funcionalidades ou só me dar um oi. 😃"""
                   })

st.image("Even-logo.png")
st.write("Uma agenda de eventos semanais com um quadro de notas comunitário. É rápido, prático e funciona direto do browser. ✅")
st.caption(f"Última atualização: {datetime.now(tz_brasil).strftime('%H:%M')}")

# selecionar página
pag = st.sidebar.radio("Selecione sua Página:", ["Ver agenda", "Criar nova agenda"])

if pag == "Ver agenda":
    agenda.render()
elif pag == "Criar nova agenda":
    submit.render()


