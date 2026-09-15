"""Hjelpefunksjoner for å hente og analysere data fra teamkatalog-tabellen i BigQuery.

Holdes utenfor Quarto-dokumentet for å gjøre koden enklere å teste og vedlikeholde,
jf. .github/instructions/quarto.instructions.md.
"""
from typing import Optional

import pandas as pd
from google.cloud import bigquery
from plotly import express as px
from plotly.graph_objs import Figure

TABLE = "pensjon-saksbehandli-prod-1f83.teamkatalogen_historikk.personer_med_tilhorighet"

# Nav sin fargepalett (fra nav-quarto-brand), brukt i alle visualiseringer.
NAV_FARGER = ["#b65681", "#457c9d", "#ad634a", "#00893c", "#ca5000", "#2176D4"]

# Renvaskede visningsnavn (uten underscore/camelCase) for kolonner som vises fram.
VISNINGSNAVN = {
    "omrade_navn": "Tilhørighet",
    "antall": "Antall",
    "andel_prosent": "Andel i prosent",
}


def hent_personer_med_tilhorighet(project: Optional[str] = None) -> pd.DataFrame:
    """Leser alle rader fra `personer_med_tilhorighet` i BigQuery og returnerer en DataFrame.

    Bruker Application Default Credentials (kjør `gcloud auth application-default login`
    lokalt før du kaller funksjonen, evt. sett GOOGLE_APPLICATION_CREDENTIALS).
    """
    client = bigquery.Client(project=project)
    query = f"select * from `{TABLE}`"
    return client.query(query).to_dataframe()


def finn_rollekolonne(df: pd.DataFrame, rolle: str) -> Optional[str]:
    """Finner kolonnen som faktisk inneholder den gitte rollen som verdi."""
    rolle_normalisert = rolle.strip().lower()
    for kolonne in df.select_dtypes(include=["object", "category"]).columns:
        verdier = df[kolonne].dropna().astype(str).str.strip().str.lower()
        if (verdier == rolle_normalisert).any():
            return kolonne
    return None


def filtrer_pa_rolle(df: pd.DataFrame, rolle: str) -> pd.DataFrame:
    """Returnerer rader der rollekolonnen matcher `rolle` (case-insensitivt)."""
    rolle_kolonne = finn_rollekolonne(df, rolle)
    if rolle_kolonne is None:
        raise ValueError(f"Fant ingen kolonne med rollen '{rolle}' i datasettet")
    rolle_normalisert = rolle.strip().lower()
    return df[df[rolle_kolonne].astype(str).str.strip().str.lower() == rolle_normalisert]


def tilhorighet_fordeling(df: pd.DataFrame, tilhorighet_kolonne: str = "omrade_navn") -> pd.DataFrame:
    """Teller antall rader per tilhørighet og beregner prosentandel."""
    fordeling = (
        df[tilhorighet_kolonne]
        .value_counts()
        .rename_axis(tilhorighet_kolonne)
        .reset_index(name="antall")
        .sort_values("antall", ascending=False)
    )
    fordeling["andel_prosent"] = (fordeling["antall"] / fordeling["antall"].sum() * 100).round(1)
    return fordeling


def plott_tilhorighet_bar(fordeling: pd.DataFrame, tilhorighet_kolonne: str = "omrade_navn", tittel: str = "") -> Figure:
    """Lager et stolpediagram over antall per tilhørighet, med renvasket tekst og Nav-farger."""
    fig = px.bar(
        fordeling,
        x=tilhorighet_kolonne,
        y="antall",
        title=tittel,
        text="antall",
        labels=VISNINGSNAVN,
        color_discrete_sequence=NAV_FARGER,
    )
    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(showlegend=False)
    return fig


def plott_tilhorighet_treemap(fordeling: pd.DataFrame, tilhorighet_kolonne: str = "omrade_navn", tittel: str = "") -> Figure:
    """Lager et treemap over andel per tilhørighet, med renvasket tekst og Nav-farger."""
    return px.treemap(
        fordeling,
        path=[tilhorighet_kolonne],
        values="antall",
        title=tittel,
        labels=VISNINGSNAVN,
        color_discrete_sequence=NAV_FARGER,
    )


def til_visningstabell(fordeling: pd.DataFrame) -> pd.DataFrame:
    """Returnerer fordelingen med renvaskede kolonnenavn, klar for visning i rapport."""
    return fordeling.rename(columns=VISNINGSNAVN)
