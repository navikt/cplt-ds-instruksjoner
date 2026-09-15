"""Utforsk og hent aggregerte data fra det federerte teamkatalogdatasettet."""

from argparse import ArgumentParser
from pathlib import Path

from google.cloud import bigquery


DATASET = "org-prod-1016.teamkatalogen_federated_query_updated_dataset"
TABLES = ("Personer", "Klynger", "Produktomraader", "Teams")
SENSITIVE_FIELD_PARTS = (
    "person",
    "ident",
    "epost",
    "email",
    "telefon",
    "navn",
    "fodsels",
    "fødsels",
)
TEAMOVERSIKT_QUERY = f"""
SELECT
  COALESCE(NULLIF(TRIM(produktomraade.name), ''), 'Ikke tilknyttet produktområde')
    AS produktomraade,
  COALESCE(NULLIF(TRIM(team.teamtype), ''), 'Ikke oppgitt') AS teamtype,
  COALESCE(NULLIF(TRIM(team.status), ''), 'Ikke oppgitt') AS status,
  COUNT(DISTINCT team.id) AS antall_team
FROM `{DATASET}.Teams` AS team
LEFT JOIN `{DATASET}.Produktomraader` AS produktomraade
  ON team.productareaid = produktomraade.id
GROUP BY 1, 2, 3
ORDER BY antall_team DESC, produktomraade, teamtype, status
"""


def parse_arguments():
    parser = ArgumentParser(
        description="Utforsk eller hent aggregerte data fra teamkatalogen."
    )
    parser.add_argument(
        "--project",
        help="GCP-prosjekt for BigQuery-jobben ved behov for eksplisitt fakturering.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser(
        "discover",
        help="Lagre tabell- og kolonnemetadata for det federerte datasettet.",
    )
    discover.add_argument(
        "--output",
        type=Path,
        default=Path("data/teamkatalogen_federert_skjema.csv"),
        help="Fil for metadata (standard: data/teamkatalogen_federert_skjema.csv).",
    )

    aggregate = subparsers.add_parser(
        "aggregate",
        help="Hent antall rader fordelt på én eller flere ikke-sensitive dimensjoner.",
    )
    aggregate.add_argument(
        "--table",
        required=True,
        help="Tabellnavn fra outputen til 'discover', uten prosjekt og datasett.",
    )
    aggregate.add_argument(
        "--dimension",
        action="append",
        required=True,
        help="Kolonne å gruppere på. Oppgi flagget flere ganger for flere dimensjoner.",
    )
    aggregate.add_argument(
        "--output",
        type=Path,
        default=Path("data/teamkatalogen_aggregert.csv"),
        help="Fil for aggregerte data (standard: data/teamkatalogen_aggregert.csv).",
    )

    teamoversikt = subparsers.add_parser(
        "teamoversikt",
        help="Hent produktområde, teamtype og status for team som et aggregert uttrekk.",
    )
    teamoversikt.add_argument(
        "--output",
        type=Path,
        default=Path("data/teamoversikt.csv"),
        help="Fil for teamoversikten (standard: data/teamoversikt.csv).",
    )
    return parser.parse_args()


def client_for(project):
    return bigquery.Client(project=project)


def discover(client, output):
    query = f"""
    SELECT
      table_name,
      column_name,
      data_type,
      is_nullable,
      ordinal_position
    FROM `{DATASET}.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name IN UNNEST(@table_names)
    ORDER BY table_name, ordinal_position
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("table_names", "STRING", TABLES)
        ]
    )
    metadata = client.query(query, job_config=job_config).to_dataframe()
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata.to_csv(output, index=False)
    print(f"Skrev metadata for {metadata['table_name'].nunique()} tabeller til {output}")


def is_sensitive(field_name):
    normalized_name = field_name.lower()
    return any(part in normalized_name for part in SENSITIVE_FIELD_PARTS)


def aggregate(client, table_name, dimensions, output):
    if table_name not in TABLES:
        raise ValueError(
            f"Ukjent tabell: {table_name}. Velg én av: {', '.join(TABLES)}"
        )

    table = client.get_table(f"{DATASET}.{table_name}")
    available_fields = {field.name for field in table.schema}
    missing_fields = sorted(set(dimensions) - available_fields)
    if missing_fields:
        raise ValueError(
            f"Kolonner finnes ikke i {table_name}: {', '.join(missing_fields)}"
        )

    sensitive_fields = [field for field in dimensions if is_sensitive(field)]
    if sensitive_fields:
        raise ValueError(
            "Kan ikke aggregere på mulig personidentifiserende kolonner: "
            f"{', '.join(sensitive_fields)}"
        )

    selected_dimensions = ",\n  ".join(f"`{field}`" for field in dimensions)
    query = f"""
    SELECT
      {selected_dimensions},
      COUNT(*) AS antall_registreringer
    FROM `{table.full_table_id}`
    GROUP BY {", ".join(str(index) for index in range(1, len(dimensions) + 1))}
    ORDER BY antall_registreringer DESC
    """
    data = client.query(query).to_dataframe()
    output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output, index=False)
    print(f"Skrev {len(data)} aggregerte rader til {output}")


def fetch_teamoversikt(client, output):
    data = client.query(TEAMOVERSIKT_QUERY).to_dataframe()
    output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output, index=False)
    print(f"Skrev {len(data)} kombinasjoner av produktområde, teamtype og status til {output}")


def main():
    arguments = parse_arguments()
    client = client_for(arguments.project)
    if arguments.command == "discover":
        discover(client, arguments.output)
    elif arguments.command == "aggregate":
        aggregate(client, arguments.table, arguments.dimension, arguments.output)
    else:
        fetch_teamoversikt(client, arguments.output)


if __name__ == "__main__":
    main()
