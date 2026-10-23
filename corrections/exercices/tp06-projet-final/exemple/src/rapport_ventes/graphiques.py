import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

NAVY = "#1F3A5F"
GREEN = "#2F7D62"
GREY = "#B8C2CC"
MILLIERS = FuncFormatter(lambda v, _: f"{v / 1000:.0f} k€")


def ca_mensuel(indicateurs: pd.DataFrame) -> Figure:
    mensuel = indicateurs.groupby("mois")["ca"].sum()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(mensuel.index, mensuel.values, marker="o", color=NAVY)
    ax.set_title("Chiffre d'affaires mensuel")
    ax.set_ylabel("chiffre d'affaires")
    ax.set_ylim(0, mensuel.max() * 1.15)
    ax.yaxis.set_major_formatter(MILLIERS)
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    return fig


def ca_par_region(indicateurs: pd.DataFrame) -> Figure:
    par_region = indicateurs.groupby("region")["ca"].sum().sort_values()
    couleurs = [GREEN if r == par_region.idxmax() else GREY for r in par_region.index]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(par_region.index, par_region.values, color=couleurs)
    part = par_region.max() / par_region.sum()
    ax.set_title(f"{par_region.idxmax()} : {part:.0%} du chiffre d'affaires")
    ax.xaxis.set_major_formatter(MILLIERS)
    ax.spines[["top", "right"]].set_visible(False)
    return fig


def taux_realisation(indicateurs: pd.DataFrame) -> Figure:
    taux = indicateurs.pivot_table(
        index="region", columns=indicateurs["mois"].dt.strftime("%m/%y"), values="taux_realisation"
    )
    fig, ax = plt.subplots(figsize=(9, 4))
    image = ax.imshow(taux.values, cmap="RdBu", vmin=0.3, vmax=1.7, aspect="auto")
    ax.set_xticks(range(taux.shape[1]), taux.columns)
    ax.set_yticks(range(taux.shape[0]), taux.index)
    for i in range(taux.shape[0]):
        for j in range(taux.shape[1]):
            valeur = taux.iloc[i, j]
            ax.text(
                j,
                i,
                f"{valeur:.0%}",
                ha="center",
                va="center",
                fontsize=8,
                color="white" if abs(valeur - 1) > 0.45 else "black",
            )
    ax.set_title("Taux de réalisation de l'objectif mensuel")
    fig.colorbar(image, ax=ax, format=FuncFormatter(lambda v, _: f"{v:.0%}"))
    return fig
