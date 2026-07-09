import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURATION DE L'APPLICATION ---
st.set_page_config(page_title="Triathlon Dashboard", page_icon="🏅", layout="centered")

st.title("🏊🚴🏃 Mon Dashboard Triathlon")
st.write("Bienvenue sur ton assistant d'entraînement adaptatif.")

# --- 2. TES IDENTIFIANTS SUPABASE ---
# (À remplacer par tes vraies clés)
SUPABASE_URL = "https://wwennpoodkxzrmmyrfeo.supabase.co"
SUPABASE_KEY = "sb_secret_rxmNy_ark1qlo1iD6PQ8fg_pFdmOHEo"

# Fonction pour se connecter à Supabase de manière optimisée
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- 3. RÉCUPÉRATION ET AFFICHAGE DES DONNÉES ---
st.header("📊 Mes Capacités Actuelles")

try:
    # On demande à Supabase la dernière ligne de notre tableau
    reponse = supabase.table("athlete_profile").select("*").order("id", desc=True).limit(1).execute()
    donnees = reponse.data

    if donnees:
        profil = donnees[0] # On prend la première (et seule) ligne récupérée
        
        # Affichage des métriques sous forme de jolies cartes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🚴 FTP Cyclisme", value=f"{profil['cyclisme_ftp']} W")
        with col2:
            st.metric(label="🏃 Allure Course", value=profil['course_allure'])
        with col3:
            st.metric(label="🏊 Allure Natation", value=profil['natation_allure'])
            
        st.caption(f"Dernière analyse Garmin : {profil['date_analyse']}")
        st.success("✅ Données synchronisées en direct depuis le Cloud !")
        
    else:
        st.info("Aucune donnée trouvée. As-tu bien exécuté ton script d'analyse ?")
        
except Exception as e:
    st.error(f"Erreur de connexion à la base de données : {e}")

# --- 4. LA SÉANCE DU JOUR (Espace pour la suite) ---
st.divider()
st.header("🎯 Ma Séance du Jour")
st.info("Bientôt ici : L'algorithme affichera ta séance adaptée automatiquement en fonction de ton sommeil de la nuit dernière !")