default:
    @just --list --unsorted


# Sjekker om nødvendige verktøy er installert. Hvis ikke, installerer med brew
bootstrap:
    uv --version > /dev/null 2>&1 || brew install uv
    quarto --version > /dev/null 2>&1 || brew install --cask quarto
    gcloud --version > /dev/null 2>&1 || brew install --cask google-cloud-sdk
    cplt --version > /dev/null 2>&1 || (brew install navikt/tap/cplt && cplt --shell-install && cplt doctor)

# Oppretter en ny gruppearbeidsmappe med skjelett fra gruppe-eksempel
init gruppenavn:
    @echo "Initialiserer gruppe: {{gruppenavn}}"
    mkdir -p {{gruppenavn}}
    cd {{gruppenavn}} && uv init --bare --description "Gruppe {{gruppenavn}} lager instruksjoner for Cplt"
    cp -r gruppe-eksempel/.github {{gruppenavn}}/
    cp gruppe-eksempel/eksempel-oppgave.md {{gruppenavn}}/
    cp gruppe-eksempel/teamkatalogen.qmd {{gruppenavn}}/
    @echo ""
    @echo "✅ Klart! Neste steg: cd inn i mappa og kjør 'cplt -d .'"

# Rendrer Quarto-rapporten i gruppemappen
render fil="teamkatalogen.qmd":
    quarto render {{fil}}