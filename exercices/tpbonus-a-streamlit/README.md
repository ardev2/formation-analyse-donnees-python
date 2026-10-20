# TP bonus A : mini tableau de bord Streamlit

## Objectif

Reprendre les indicateurs et les graphiques produits dans les TP précédents, et les exposer dans une application Streamlit avec au moins un filtre interactif.

## Livrable

Une application Streamlit fonctionnelle, lancée en local avec `streamlit run`.

## Les données

Le dossier `ressources/` contient les deux tables produites au TP3 :

- `indicateurs_mois_region.parquet` : une ligne par mois et par région, avec le chiffre d'affaires, le nombre de commandes, l'objectif et le taux de réalisation ;
- `ventes_consolidees.parquet` : une ligne par commande, avec le produit, la catégorie, la région et le montant.

---

## Étape 0 : lancer l'application de départ

```bash
uv sync
uv run streamlit run app.py
```

Le navigateur s'ouvre sur l'application, qui affiche pour l'instant un titre et le nombre de ventes. Laisse-la ouverte : à chaque enregistrement de `app.py`, Streamlit propose de recharger la page (choisis *Always rerun*).

## Étape 1 : les filtres

Dans la sidebar (`st.sidebar`), ajoute :

- une sélection de régions avec `st.sidebar.multiselect`, toutes les régions étant sélectionnées par défaut ;
- une période avec `st.sidebar.select_slider`, sur la liste des mois au format `AAAA-MM`, avec deux bornes ;
- une sélection de catégories, facultative.

Filtre ensuite les deux tables selon ces choix. Si la sélection ne contient aucune vente, affiche un message avec `st.warning` et arrête le script avec `st.stop()`.

## Étape 2 : les chiffres clés

Sur une ligne de trois colonnes (`st.columns(3)`), affiche avec `st.metric` le chiffre d'affaires, le nombre de commandes et le panier moyen de la sélection.

Résultat attendu, avec toutes les régions, toutes les catégories et toute la période : un chiffre d'affaires de 409 501,59 euros, 2182 commandes et un panier moyen de 187,67 euros. Avec la seule région Île-de-France : 127 936,94 euros.

## Étape 3 : le graphique principal

Affiche avec plotly express, déjà déclaré dans `pyproject.toml`, l'évolution du chiffre d'affaires mensuel par région, avec `st.plotly_chart`. Il doit suivre les filtres.

## Étape 4 : les objectifs et les produits

Sur deux colonnes :

- à gauche, un tableau (`st.dataframe`) du chiffre d'affaires, de l'objectif cumulé et du taux de réalisation par région, sur la période choisie ;
- à droite, les cinq produits qui rapportent le plus, en graphique ou en tableau.

## Pour aller plus loin

- Un bouton `st.download_button` pour télécharger les ventes sélectionnées en CSV.
- Des onglets avec `st.tabs` : vue d'ensemble, régions, produits.
- Une mise en forme des colonnes du tableau avec `column_config` : montants en euros, barre de progression pour le taux de réalisation.

## Avant de rendre

- `uv run streamlit run app.py` lance l'application sans erreur.
- Chaque filtre modifie les chiffres clés, le graphique et les tableaux.
- Une sélection vide affiche un message plutôt qu'une erreur.
- Les données ne sont lues qu'une fois grâce à `@st.cache_data`.
