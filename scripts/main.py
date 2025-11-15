import streamlit as st
import pycron
import time
from requests import get
from env_vars import ENV

if ENV == 'DEV':
    from sqlite_connection import save_to_sqlite as save_to_db
elif ENV == 'PROD':
    from supabase_conection import save_to_supabase as save_to_db

def remove_streamlit_hamburguer():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():

    st.set_page_config(
        page_title="Renata 40 Anos - Confirme presença nesta festança",
        page_icon=":beers:",
        menu_items={}  # Disable the hamburger menu
    )

    remove_streamlit_hamburguer()

    st.title(":tada: Renata 40 Anos! :beers:")

    st.write(f"**Confirme presença nesta festança**")

    # Sponsor's name
    sponsor_name = st.text_input("Convidado:", placeholder="Preencha seu nome!", key="sponsor_name")

    # Number of people
    companions_total = st.number_input("Convidado(s) Acompanhante(s):", min_value=0, step=1, key="companions_total")

    # Dynamic fields for names based on the number of people
    companions = []
    for i in range(companions_total):
        name = st.text_input(f"Nome do {i + 1}° acompanhante:", placeholder=f"Nome da {i + 1}° acompanhante", key=f"person_{i}")
        companions.append(name)

    # Submit button
    submitted = st.button("Enviar")

    # Handle form submission
    if submitted:
        if not sponsor_name.strip():
            st.error("Por favor, preencha seu nome.")
        elif any(not name.strip() for name in companions):
            st.error("Por favor, preencha todos os nomes.")
        else:
            total = companions_total + 1
            if save_to_db(st, sponsor_name, companions, total):

                st.success(f"Obrigado pela sua confirmação {sponsor_name}!")
                if companions_total > 0:
                    st.write(f"**Acompanhantes:**")
                    for i, name in enumerate(companions, start=1):
                        st.success(f"{i}. {name}")

if __name__ == "__main__":
    main()

    while True:
        if pycron.is_now('*/13 * * * *'):   # True Every Sunday at 02:00
            print('running render')
            response = get("https://birthday-confirmation.onrender.com/")
            print(f'Render response status code: {response.status_code}')
        if pycron.is_now('0 0 * * 0'):
            pass
