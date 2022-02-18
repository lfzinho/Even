import datetime
import streamlit as st
import pymongo

dias_da_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

banco = "Even"
client = pymongo.MongoClient(st.secrets["mongo_string1"]+banco+st.secrets["mongo_string2"])
db = client[banco]

def render():
    agenda = st.text_input("Nome da agenda:")
    criador = st.text_input("Seu nome:")

    # container de tipos
    with st.container():
        st.markdown("---")
        st.title("Tipos de eventos")
        n_eventos = st.number_input("Selecione a quantidade de eventos", 0, 25, 3, 1)
        
        with st.form("Eventos"):
            all_types = {}
            #cria eventos individuais
            for i in range(n_eventos):
                d_type = {}
                with st.expander(f"Evento #{i+1}:", True if i==0 else False):
                    name = st.text_input("Nome do evento:", key=i)
                    
                    s_desc = st.text_input("Sediador do evento: (Ex.: nome do professor.)", key=i*10)

                    link = st.text_input("Link do evento:", key=i*20)

                    l_desc = st.text_area("Descrição longa do evento: (Apenas insira se necessário.)", key=i)

                    d_type["name"] = name
                    d_type["s_desc"] = s_desc
                    d_type["link"] = link
                    d_type["l_desc"] = l_desc
                all_types[str(i+1)] = d_type

            st.form_submit_button("Salvar")

    # container de ocorrências
    with st.container():
        st.markdown("---")
        st.title("Ocorrência de eventos")
        n_ocorr = st.number_input("Selecione a quantidade de ocorrências", 0, 25, 3, 1)
        
        with st.form("Ocorrências"):
            
            #cria eventos individuais
            all_ocor = {}
            for i in range(n_ocorr):
                d_ocor = {}
                with st.expander(f"Ocorrência #{i+1}:", True):
                    t_even = st.number_input("Escolha o # do evento:", 1, 25, 1, 1, key=-i)

                    dia = st.selectbox("Selecione o dia da semana:", dias_da_semana, key=-i)

                    col1, col2 = st.columns(2)
                    with col1:
                        inicio = st.time_input("Horário de início:", datetime.time(0, 0), key=i)
                    with col2:
                        fim = st.time_input("Horário de término:", datetime.time(0, 0), key=i*10)

                    d_ocor["tipo"] = str(t_even)
                    d_ocor["timestamp"] = get_min(inicio, day=dia)
                    d_ocor["dia"] = dia
                    d_ocor["inicio"] = get_min(inicio)
                    d_ocor["fim"] = get_min(fim)
                all_ocor[str(i+1)] = d_ocor

            st.form_submit_button("Salvar")
    
    # envio final
    st.markdown("---")
    col1, col2 = st.columns(2)
    scs_msg = st.container()
    with col1:
        st.write("Quando estiver com tudo configurado, clique em enviar.")
    with col2:
        if st.button("Enviar", key=42):
            
            agenda = {
                    "name":agenda,
                    "creator":criador,
                    "tipos": all_types,
                    "ocorrs": order_ocorrs(all_ocor)}

            with st.spinner("Aguarde, estamos enviando os dados..."):
                db["agendas"].insert_one(agenda)
                pass
            
            scs_msg.success("Parabéns! Sua agenda foi registrada!")
            exp_sent = scs_msg.expander("Ver arquivo enviado:")
            exp_sent.write(agenda)

            st.balloons()

# transforma os marcadores de tempo em minutos  
def get_min(time, day="Domingo"):
    day_min = dias_da_semana.index(day)*24*60
    time_min = time.hour*60 + time.minute
    return str(day_min +time_min)

# ordena as ocorrências
def order_ocorrs(all):
    result = {}
    timestamps = []
    for ocor in all:
        timestamps.append( int(all[ocor]["timestamp"]) )
    timestamps.sort() # ordena os tstamps dos eventos
    
    for tstamp in timestamps: # pra cada horário
        for ocor in all: # verifica se a ocorrencia é igual
            if all[ocor]["timestamp"] == str(tstamp):

                clean_ocor = all[ocor].copy() #remove a var de contas
                clean_ocor.pop("timestamp")
                
                result[str(len(result)+1)] = clean_ocor
                break # add no result e vai pro próximo
    
    return result
    