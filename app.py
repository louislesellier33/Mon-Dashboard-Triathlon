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

st.header("🎯 Ma Séance du Jour")

try:
    # On demande à Supabase la dernière ligne de notre tableau du jour
    reponse_jour = supabase.table("daily_status").select("*").order("id", desc=True).limit(1).execute()
    donnees_jour = reponse_jour.data

    if donnees_jour:
        statut = donnees_jour[0]
        
        # Affichage du score
        st.subheader(f"{statut['etat_fatigue']}")
        st.metric(label="💤 Score de Sommeil Garmin", value=f"{statut['score_sommeil']} / 100")
        
        # Affichage de la recommandation avec la bonne couleur
        if "🟢" in statut['etat_fatigue']:
            st.success(f"**Prescription du Coach :** {statut['seance_recommandee']}")
        elif "🟠" in statut['etat_fatigue']:
            st.warning(f"**Prescription du Coach :** {statut['seance_recommandee']}")
        else:
            st.error(f"**Prescription du Coach :** {statut['seance_recommandee']}")
            
        st.caption(f"Analyse basée sur ta nuit du {statut['date_jour']}")
    else:
        st.info("Aucune séance calculée pour aujourd'hui. L'algorithme n'a pas encore tourné !")
        
except Exception as e:
    st.error(f"Erreur lors de la récupération de la séance du jour : {e}")