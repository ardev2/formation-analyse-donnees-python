import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ventes 2025", layout="wide")


@st.cache_data
def charger_donnees() -> tuple[pd.DataFrame, pd.DataFrame]:
    indicateurs = pd.read_parquet("ressources/indicateurs_mois_region.parquet")
    ventes = pd.read_parquet("ressources/ventes_consolidees.parquet")
    return indicateurs, ventes


indicateurs, ventes = charger_donnees()

st.title("Tableau de bord des ventes 2025")
st.write(f"{len(ventes)} ventes chargées, de {ventes['date'].min():%d/%m/%Y} au {ventes['date'].max():%d/%m/%Y}.")

# TODO étape 1 : les filtres dans la sidebar
# TODO étape 2 : les chiffres clés
# TODO étape 3 : le graphique principal
# TODO étape 4 : les objectifs et les produits
