import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Ventes 2025", layout="wide")


@st.cache_data
def charger_donnees() -> tuple[pd.DataFrame, pd.DataFrame]:
    indicateurs = pd.read_parquet("ressources/indicateurs_mois_region.parquet")
    ventes = pd.read_parquet("ressources/ventes_consolidees.parquet")
    return indicateurs, ventes


def euros(valeur: float) -> str:
    return f"{valeur:,.0f} €".replace(",", " ")


indicateurs, ventes = charger_donnees()

st.title("Tableau de bord des ventes 2025")

toutes_regions = sorted(indicateurs["region"].unique())
regions = st.sidebar.multiselect("Régions", toutes_regions, default=toutes_regions)
mois = sorted(indicateurs["mois"].dt.strftime("%Y-%m").unique())
debut, fin = st.sidebar.select_slider("Période", options=mois, value=(mois[0], mois[-1]))
categories = st.sidebar.multiselect("Catégories", sorted(ventes["categorie"].unique()), default=None)

masque_mois = indicateurs["mois"].dt.strftime("%Y-%m").between(debut, fin)
ind = indicateurs[masque_mois & indicateurs["region"].isin(regions)]

masque_ventes = ventes["date"].dt.strftime("%Y-%m").between(debut, fin) & ventes["region"].isin(regions)
if categories:
    masque_ventes &= ventes["categorie"].isin(categories)
v = ventes[masque_ventes]

if v.empty:
    st.warning("Aucune vente pour cette sélection.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Chiffre d'affaires", euros(v["montant"].sum()))
col2.metric("Commandes", f"{len(v):,}".replace(",", " "))
col3.metric("Panier moyen", euros(v["montant"].mean()))

mensuel = v.groupby([v["date"].dt.to_period("M").dt.to_timestamp().rename("mois"), "region"], as_index=False)[
    "montant"
].sum()
fig = px.line(
    mensuel,
    x="mois",
    y="montant",
    color="region",
    markers=True,
    labels={"mois": "", "montant": "chiffre d'affaires (euros)", "region": "région"},
    title="Chiffre d'affaires mensuel",
)
st.plotly_chart(fig, width="stretch")

gauche, droite = st.columns(2)
with gauche:
    st.subheader("Objectifs")
    taux = ind.groupby("region")[["ca", "objectif_mensuel"]].sum()
    taux["taux_realisation"] = taux["ca"] / taux["objectif_mensuel"]
    st.dataframe(
        taux.sort_values("taux_realisation", ascending=False),
        column_config={
            "ca": st.column_config.NumberColumn("chiffre d'affaires", format="%.0f €"),
            "objectif_mensuel": st.column_config.NumberColumn("objectif cumulé", format="%.0f €"),
            "taux_realisation": st.column_config.ProgressColumn(
                "réalisé", min_value=0, max_value=1.5, format="percent"
            ),
        },
    )
with droite:
    st.subheader("Produits")
    top = v.groupby("produit", as_index=False)["montant"].sum().nlargest(5, "montant")
    st.bar_chart(top, x="produit", y="montant", horizontal=True)

st.download_button(
    "Télécharger les ventes sélectionnées (CSV)",
    v.to_csv(index=False).encode("utf-8"),
    file_name="ventes_selection.csv",
    mime="text/csv",
)
