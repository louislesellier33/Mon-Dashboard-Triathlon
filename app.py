import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURATION DE L'APPLICATION ---
st.set_page_config(page_title="Triathlon Dashboard", page_icon="🏅", layout="centered")

st.title("🏊🚴🏃 Mon Dashboard Triathlon")
st.write("Bienvenue sur ton assistant d'entraînement adaptatif.")

# --- 2. TES IDENTIFIANTS SUPABASE ---
SUPABASE_URL = "https://wwennpoodkxzrmmyrfeo.supabase.co"
SUPABASE_KEY = "sb_publishable_fFuP3gn6m5o0qT1XMKiSCQ_6oUTOTo4"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- 3. RÉCUPÉRATION ET AFFICHAGE DES DONNÉES ---
st.header("📊 Mes Capacités Actuelles")

try:
    reponse = supabase.table("athlete_profile").select("*").order("id", desc=True).limit(1).execute()
    donnees = reponse.data

    if donnees:
        profil = donnees[0]
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

# --- 4. LA SÉANCE DU JOUR (ADAPTATIVE) ---
st.divider()
st.header("🎯 Ma Séance du Jour")

try:
    reponse_jour = supabase.table("daily_status").select("*").order("id", desc=True).limit(1).execute()
    donnees_jour = reponse_jour.data

    if donnees_jour:
        statut = donnees_jour[0]
        
        st.subheader(f"{statut['etat_fatigue']}")
        st.metric(label="💤 Score de Sommeil Garmin", value=f"{statut['score_sommeil']} / 100")
        
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

# --- 5. MON OBJECTIF SPORTIF ---
st.divider()
st.header("🏁 Mon Objectif Principal")
st.write("Défini ta prochaine course et tes allures cibles. Le plan s'adaptera pour combler l'écart entre ton niveau actuel et cet objectif.")

try:
    reponse_obj = supabase.table("race_objective").select("*").order("id", desc=True).limit(1).execute()
    dernier_obj = reponse_obj.data
    
    if dernier_obj:
        obj = dernier_obj[0]
        st.success(f"**Objectif actuel :** Triathlon {obj['distance']} le {obj['date_course']}")
        c1, c2, c3 = st.columns(3)
        c1.caption(f"🏊 Cible : {obj['allure_natation_cible']}")
        c2.caption(f"🚴 Cible : {obj['vitesse_velo_cible']}")
        c3.caption(f"🏃 Cible : {obj['allure_course_cible']}")
except:
    pass

with st.expander("✏️ Définir ou modifier mon objectif"):
    with st.form("formulaire_objectif"):
        st.subheader("1. La Course")
        col1, col2 = st.columns(2)
        with col1:
            distance = st.selectbox("Format du Triathlon", ["XS", "S", "M", "Half-Ironman", "Ironman"])
        with col2:
            date_course = st.date_input("Date de la course")

        st.subheader("2. Mes Cibles (Allure/Vitesse)")
        col_nat, col_velo, col_run = st.columns(3)
        with col_nat:
            cible_nat = st.text_input("🏊 Natation (ex: 1:45/100m)", value="1:45/100m")
        with col_velo:
            cible_velo = st.text_input("🚴 Vélo (ex: 30 km/h)", value="30 km/h")
        with col_run:
            cible_run = st.text_input("🏃 Course (ex: 4:30/km)", value="4:30/km")

        soumis = st.form_submit_button("Enregistrer mon objectif")

        if soumis:
            try:
                donnees_objectif = {
                    "distance": distance,
                    "date_course": str(date_course),
                    "allure_natation_cible": cible_nat,
                    "vitesse_velo_cible": cible_velo,
                    "allure_course_cible": cible_run
                }
                supabase.table("race_objective").insert(donnees_objectif).execute()
                st.success("✅ Objectif enregistré ! Recharge la page pour le voir apparaître.")
            except Exception as e:
                st.error(f"Erreur d'enregistrement : {e}")
