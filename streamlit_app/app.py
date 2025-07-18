import os
import streamlit as st
import pandas as pd
from scraping_funcs import scrape_voitures, scrape_motos, scrape_locations
import plotly.express as px

st.set_page_config(page_title="Auto Dakar Scraper", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff; /* Fond blanc sobre */
            color: #2c3e50; /* Texte foncé */
        }
        .stSidebar {
            background-color: #f0f2f6;
        }
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 0.6rem 1.2rem;
        }
        .stDownloadButton > button {
            background-color: #2e8b57; /* Vert foncé */
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 0.6rem 1.2rem;
        }
        .stRadio > label {
            font-weight: 500;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }

    </style>
""", unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🚗 Auto Dakar Data App</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; margin-top: -10px; margin-bottom: 30px;'>
        <p style='font-size: 18px; color: #374151;'>
            Cette application permet de scraper des données à partir du site <b>Dakar-Auto</b> sur plusieurs pages, 
            ou d’afficher les fichiers CSV déjà collectés via <b>Web Scraper</b> sans avoir à relancer le scraping.
        </p>
        <p style='font-size: 16px; color: #4B5563;'>
            📚 <i>Librairies utilisées : pandas, streamlit, selenium, beautifulsoup4</i><br>
            🌐 <i>Source des données : <a href='https://dakar-auto.com' target='_blank'>Dakar-Auto.com</a></i>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.header("🔧 Paramètres")
pages = st.sidebar.number_input("Nombre de pages (pagination)", min_value=1, max_value=600, value=2)
option = st.sidebar.selectbox("Choisissez une option",
                              ["Scrape data", "Télécharger données brutes", "Afficher formulaire", "Dashboard"])

if option == "Télécharger données brutes":
    st.subheader("📥 Affichage des données Web Scraper (non nettoyées)")
    data_type = st.sidebar.radio("Type de données", ["Voitures", "Motos & Scooters", "Location de voitures"])

    if st.button(f"Afficher données brutes {data_type}"):
        file_map = {
            "Voitures": "voitures.csv",
            "Motos & Scooters": "motos.csv",
            "Location de voitures": "locations.csv"
        }

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw")

        file_path = os.path.join(DATA_DIR, file_map[data_type])
        try:
            df = pd.read_csv(file_path)
            st.markdown(f"""
            <div style='background-color: #e8f4ea; padding: 12px; border-radius: 8px; margin-bottom: 15px; color: #2e7d32; font-size: 16px;'>
                ✅ <strong>{len(df)} lignes chargées depuis <i>{file_map[data_type]}</i></strong>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(df, use_container_width=True)
        except FileNotFoundError:
            st.error(f"❌ Le fichier {file_map[data_type]} est introuvable dans /data/raw")

elif option == "Scrape data":
    st.subheader("🔍 Scraping automatique des données depuis Dakar-Auto")

    if st.button("🚗 Scrape Voitures"):
        df_voitures = scrape_voitures(pages)
        st.success(f"{len(df_voitures)} annonces récupérées")
        st.dataframe(df_voitures, use_container_width=True)
        csv = df_voitures.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger Voitures CSV", csv, "voitures.csv", "text/csv")

    if st.button("🏍️ Scrape Motos & Scooters"):
        df_motos = scrape_motos(pages)
        st.success(f"{len(df_motos)} annonces récupérées")
        st.dataframe(df_motos, use_container_width=True)
        csv = df_motos.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger Motos CSV", csv, "motos.csv", "text/csv")

    if st.button("🚘 Scrape Locations"):
        df_locations = scrape_locations(pages)
        st.success(f"{len(df_locations)} annonces récupérées")
        st.dataframe(df_locations, use_container_width=True)
        csv = df_locations.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger Locations CSV", csv, "locations.csv", "text/csv")

elif option == "Afficher formulaire":
    st.subheader("📝 Remplir le formulaire Kobotoolbox")

    st.markdown("""
            <iframe src="https://ee.kobotoolbox.org/i/rlgLziTC" width="100%" height="700" style="border:none;"></iframe>
        """, unsafe_allow_html=True)

elif option == "Dashboard":
    st.subheader("📊 Dashboard - Analyse des données nettoyées")

    tab1, tab2, tab3 = st.tabs(["🚗 Voitures", "🏍️ Motos", "🚘 Voitures d'occasion"])

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")

    # Onglet Voitures
    with tab1:
        st.markdown("### Statistiques sur les voitures")
        try:
            df_voitures = pd.read_csv(os.path.join(CLEANED_DIR, "voitures_clean.csv"))
            df_voitures["prix"] = pd.to_numeric(df_voitures["prix"], errors="coerce")
            df_voitures["kilometrage"] = pd.to_numeric(df_voitures["kilometrage"], errors="coerce")

            st.markdown("#### 💰 Prix moyen par marque")
            prix_moyen = df_voitures.groupby("marque")["prix"].mean().sort_values(ascending=False).head(10)
            st.bar_chart(prix_moyen)

            st.markdown("#### ⛽ Répartition des types de carburant")
            carburants = df_voitures["carburant"].value_counts()
            st.dataframe(carburants.rename("Nombre"))
            st.plotly_chart(px.pie(df_voitures, names="carburant", title="Répartition par carburant"))

            st.markdown("#### 📉 Prix vs Kilométrage")
            st.plotly_chart(px.scatter(
                df_voitures,
                x="kilometrage",
                y="prix",
                color="marque",
                title="Relation Kilométrage / Prix"
            ))

        except FileNotFoundError:
            st.error("Fichier voitures_clean.csv introuvable.")

    # Onglet Motos
    with tab2:
        st.markdown("### Statistiques sur les motos")
        try:
            df_motos = pd.read_csv(os.path.join(CLEANED_DIR, "motos_clean.csv"))
            df_motos["prix"] = pd.to_numeric(df_motos["prix"], errors="coerce")
            df_motos["kilometrage"] = pd.to_numeric(df_motos["kilometrage"], errors="coerce")

            st.markdown("#### 💰 Prix moyen par marque")
            prix_moyen_moto = df_motos.groupby("marque")["prix"].mean().sort_values(ascending=False).head(10)
            st.bar_chart(prix_moyen_moto)

            st.markdown("#### 📉 Prix vs Kilométrage")
            st.plotly_chart(px.scatter(
                df_motos,
                x="kilometrage",
                y="prix",
                color="marque",
                title="Relation Kilométrage / Prix"
            ))

        except FileNotFoundError:
            st.error("Fichier motos_clean.csv introuvable.")

    # Onglet Voitures d'occasion
    with tab3:
        st.markdown("### Statistiques sur les voitures d’occasion")
        try:
            df_location = pd.read_csv(os.path.join(CLEANED_DIR, "locations_clean.csv"))
            df_location["prix"] = pd.to_numeric(df_location["prix"], errors="coerce")

            st.markdown("#### 💰 Prix moyen par marque")
            prix_moyen_loc = df_location.groupby("marque")["prix"].mean().sort_values(ascending=False).head(10)
            st.bar_chart(prix_moyen_loc)

            st.markdown("#### 📍 Répartition par adresse")
            repartition_adresse = df_location["adresse"].value_counts().head(10)
            st.bar_chart(repartition_adresse)

        except FileNotFoundError:
            st.error("Fichier locations_clean.csv introuvable.")
