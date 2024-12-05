import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd

# Lecture du fichier CSV
@st.cache_data
def charger_donnees_csv(fichier):
    return pd.read_csv(fichier)

# Charger les données
fichier_csv = "authentification.csv"
donnees_comptes = charger_donnees_csv(fichier_csv)

def convertir_en_dict(donnees):
    comptes = {}
    for _, ligne in donnees.iterrows():
        comptes[ligne['name']] = {
            'name': ligne['name'],
            'password': ligne['password'],
            'email': ligne['email'],
            'failed_login_attempts': ligne['failed_login_attempts'],
            'logged_in': ligne['logged_in'],
            'role': ligne['role']
        }
    return {'usernames': comptes}

# Convertir les données pour l'authentificateur
lesDonneesDesComptes = convertir_en_dict(donnees_comptes)

authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie name",
    "cookie key",
    30
)

authenticator.login()

def accueil():
    st.title("Vous avez accès au contenu réservé aux utilisateurs connectés")

# Si l'utilisateur est authentifié
if st.session_state["authentication_status"]:
    accueil()
    st.image("Bravo.jpg", use_column_width=True)

    # Création du menu dans la barre latérale
    with st.sidebar:
        st.write('Bienvenue! 👋')
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Photos", "Vidéos"],
            icons=["house", "camera", "film"],
            menu_icon="cast"
        )

        # Bouton de déconnexion
        authenticator.logout("Déconnexion")

    # Gestion des pages selon la sélection
    if selection == "Accueil":
        st.title("Bienvenue sur la page d'accueil 🏠")
    elif selection == "Photos":
        st.title("Bienvenue sur l'album photo chats 😽:heart_eyes_cat:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("chat1.jpg", use_column_width=True)
        with col2:
            st.image("chat2.jpg", use_column_width=True)
        with col3:
            st.image("chat3.jpg", use_column_width=True)
    elif selection == "Vidéos":
        st.title("Bienvenue sur la page des vidéos 🎬")

# Si l'utilisateur n'est pas authentifié
elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Les champs username et mot de passe doivent être remplis")

