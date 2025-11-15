import streamlit as st
import os
import pycron
import time
from requests import get
from env_vars import ENV
import streamlit.components.v1 as components
from datetime import datetime


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
        page_title="Renata 40 Anos - Axé & Churrasco",
        page_icon="🎉",
        menu_items={}
    )

    remove_streamlit_hamburguer()

    # 🎤 Cabeçalho da festa
    st.title("🎉 Renata 40 Anos! 😎✨")
    st.subheader("Festa no ritmo do Axé + Churrasco! 🍖🎶")

    st.markdown("""
    **O Sol vai brilhar (e se chover terá tenda!!), o axé vai comandar e vou comemorar 40 anos!**
    Música boa, chopp gelado e gente bonita formadora de opinião!! 💛
    """)

    st.markdown("---")

    # ✍️ Formulário de Confirmação
    st.header("Confirme sua presença! ✍️")

    sponsor_name = st.text_input("Seu nome:", placeholder="Preencha seu nome", key="sponsor_name")
    companions_total = st.number_input("Número de acompanhantes:", min_value=0, step=1, key="companions_total")

    companions = []
    for i in range(companions_total):
        name = st.text_input(
            f"Nome do {i + 1}° acompanhante:",
            placeholder=f"Nome do {i + 1}° acompanhante",
            key=f"companion_{i}"
        )
        companions.append(name)

    submitted = st.button("Enviar confirmação 🎯")

    if submitted:
        if not sponsor_name.strip():
            st.error("Por favor, preencha seu nome.")
        elif any(not name.strip() for name in companions):
            st.error("Por favor, preencha todos os nomes dos acompanhantes.")
        else:
            total = companions_total + 1

            if save_to_db(st, sponsor_name, companions, total):
                st.balloons()
                st.success(f"Êeeee {sponsor_name}. Fiquei super feliz em saber que você não vai ficar de fora dessa! 💃🪩⚡")

                if companions_total > 0:
                    st.write("**Acompanhantes:**")
                    for i, name in enumerate(companions, start=1):
                        st.write(f"{i}. {name}")

    st.markdown("---")

    # Informações do evento
    st.markdown("""
    ### Informações da Festa

    **📅 Data:** 13/12/2025.

    **🕑 Horário:** A partir das 14h.

    **📍 Local:** Rua Seis, 225-C, Quintas do Godoy, Betim-MG.

    **🍖 Churrasco e 🍻 Bebida gelada!**

    👗 **Dress code:** Look leve para dançar muito axé! 💃🕺
    """)

    google_maps_iframe = """
    <iframe src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3628.609887624522!2d-44.242393!3d-19.936913!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMTnCsDU2JzEyLjkiUyA0NMKwMTQnMzIuNiJX!5e1!3m2!1sen!2sbr!4v1763242450903!5m2!1sen!2sbr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    """

    # <iframe src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3628.609887624522!2d-44.242393!3d-19.936913!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMTnCsDU2JzEyLjkiUyA0NMKwMTQnMzIuNiJX!5e1!3m2!1sen!2sbr!4v1763242450903!5m2!1sen!2sbr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>

    # https://www.google.com/maps/place/19%C2%B056'12.9%22S+44%C2%B014'32.6%22W/@-19.936913,-44.242393,797m/data=!3m2!1e3!4b1!4m4!3m3!8m2!3d-19.936913!4d-44.242393!17m2!4m1!1e3!18m1!1e1

    components.html(google_maps_iframe, height=375, width=500)

    # Google Maps link
    st.markdown(
        "[📍 Abrir localização no Google Maps](https://www.google.com/maps/place/19%C2%B056'12.9%22S+44%C2%B014'32.6%22W/@-19.936913,-44.242393,833m/data=!3m1!1e3!4m4!3m3!8m2!3d-19.936913!4d-44.242393!17m2!4m1!1e3!18m1!1e1?entry=ttu&g_ep=EgoyMDI1MTExMi4wIKXMDSoASAFQAw%3D%3D)",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Contador regressivo
    party_date = datetime(2025, 12, 13, 14, 0, 0)  # 13/12/2025 às 14:00
    now = datetime.now()

    days_left = (party_date - now).days

    if days_left > 0:
        st.markdown(f"""
        ## ⏳ Contagem Regressiva
        **Faltam `{days_left}` dia(s) para minha festa de 40 Anos!** 🎉🔥
        Prepare o quadril, porque vai ter muito axé! 💃🪩
        """)
    else:
        st.markdown("""
        ## 🎊 Chegou o grande dia!!!
        Bora comemorar com muito Axé e Churrasco! 🍖🎶
        """)


if __name__ == "__main__":
    main()

    # while True:

    #     if pycron.is_now('*/5 * * * *'):   # True Every Sunday at 02:00
    #         print('running render')
    #         response = get("https://birthday-confirmation.onrender.com/")
    #         print(f'Render response status code: {response.status_code}')
    #         time.sleep(60)
    #     if pycron.is_now('0 0 * * 0'):
    #         print('running supabase')
    #         os.system('python scripts/supabase_api.py')
