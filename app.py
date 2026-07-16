# --- 5. MON OBJECTIF SPORTIF ---
st.divider()
st.header("🏁 Mon Objectif Principal")
st.write("Défini ta prochaine course et tes allures cibles. Le plan s'adaptera pour combler l'écart entre ton niveau actuel et cet objectif.")

# On récupère le dernier objectif enregistré pour l'afficher
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

# Le formulaire pour créer ou modifier l'objectif
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
