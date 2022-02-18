import streamlit as st
import datetime
import pymongo
import math

dias_da_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
evento_vazio = {
    "name":"Sem eventos pela semana :)",
    "horario":"0:00 - 0:00",
    "s_desc":":)",
    "link":"",
    "l_desc":"",
    "dia":"--"
}


banco = "Even"
client = pymongo.MongoClient(st.secrets["mongo_string1"]+banco+st.secrets["mongo_string2"])
db = client[banco]

def get_min(time, day="Domingo"):
    day_min = dias_da_semana.index(day)*24*60
    time_min = time.hour*60 + time.minute
    return str(day_min +time_min)

# completa os minutos se der um número de 1 algarismo só
def fill_str(str):
    if len(str) < 2:
        return "0"+str
    else:
        return str

class class_agenda:
    now = get_min(datetime.datetime.now(), dias_da_semana[datetime.datetime.today().weekday()+1])

    def __init__(self, mongo_query) -> None:
        self.mongo_query = mongo_query
        self.data = {}

        self.events = []
        self.creator = ""
    
    def bake(self):
        for elem in self.mongo_query:
            self.data = elem

        self.creator = self.data['creator']
        
        # Procura pelo primeiro evento futuro. Mostra o evento por até 60 minutos depois do início.
        elem_saver = 0
        for elem in self.data["ocorrs"]:
            if int(self.data["ocorrs"][elem]["inicio"]) + \
                dias_da_semana.index(self.data["ocorrs"][elem]["dia"])*24*60 \
                + 60 - int(self.now) >= 0:

                evento =  self.data["tipos"][ self.data["ocorrs"][elem]["tipo"] ].copy()

                # converte os dados de início e fim para str:horario em evento
                inicio = str(math.floor(int(self.data["ocorrs"][elem]["inicio"])/60))+":"+fill_str(str(int(self.data["ocorrs"][elem]["inicio"])%60))
                fim = str(math.floor(int(self.data["ocorrs"][elem]["fim"])/60))+":"+fill_str(str(int(self.data["ocorrs"][elem]["fim"])%60))
                evento["horario"] = inicio+" - "+fim
                evento["dia"] = self.data["ocorrs"][elem]["dia"]

                # adiciona o evento
                self.events.append( evento )
                elem_saver += 1

                if elem_saver == 3: # salva no max 4 elementos
                    break
        
        if elem_saver <= 3: # se n tem elems o suficiente pra fechar a agenda
            while len(self.events) < 4:
                self.events.append(evento_vazio)

        return self



def render():
    # selecione a sua agenda
    agenda_name = st.selectbox("Selecione a sua agenda:", get_a_names())

    # cálculos de agenda
    agenda = class_agenda( db["agendas"].find({"name":agenda_name}) ).bake()

    st.markdown("---\n\n#")

    # seção de notas comunitárias
    notas = db["notas"].find_one({"name":agenda_name})
    if notas is None:
        db["notas"].insert_one({"name":agenda_name, "texto":"Sem notas."})
        notas = {"texto":"Sem notas."}

    notas_update = st.text_area("Notas comunitárias", notas["texto"])

    # editando as notas
    if st.button("Atualizar notas"):
        with st.spinner("Aguarde, estamos enviando os dados..."):
            nota = {"name": agenda_name,
            "texto": notas_update}

            db["notas"].update_one({'name':agenda_name}, {"$set":{'texto':notas_update}})
        st.success("Notas comunitárias atualizadas!")


    # evento principal
    evento = agenda.events[0]
    with st.container():
        st.caption("Evento de agora:")

        col1, col2 = st.columns(2)
        with col1:
            st.title(evento["name"])
        with col2:
            st.title(evento["horario"])
        st.markdown(f"[Entrar no link]({evento['link']})")

        st.subheader(evento['s_desc'])
        st.caption(evento['l_desc'])
        st.markdown("---")

    st.markdown("#") # espaço em branco
    st.markdown("#")

    # proximos eventos
    with st.container():
        st.caption("Próximos eventos:")

        col1, col2, col3 = st.columns(3)
        
        evento = agenda.events[1]
        with col1:
            st.write(evento['horario'])
            st.subheader(evento['name'])
            st.caption(evento['dia'])
        
        evento = agenda.events[2]
        with col2:
            st.write(evento['horario'])
            st.subheader(evento['name'])
            st.caption(evento['dia'])

        evento = agenda.events[3]
        with col3:
            st.write(evento['horario'])
            st.subheader(evento['name'])
            st.caption(evento['dia'])
    
    st.caption(f"Agenda criada por {agenda.creator}.")


def get_a_names():
    query = db["agendas"].find({})
    result = []
    for elem in query:
        result.append(elem["name"])
    
    return result




