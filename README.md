# 🤖 cplt-ds-instruksjoner

Et praktisk verksted for data scientists i Nav, der vi utforsker hvordan instruksjonsfiler kan gjøre cplt mer nyttig i arbeidshverdagen.

# HØRA

## Hensikt

Lage og teste om instruksjoner gjør cplt bedre tilpasset DS-arbeidsoppgaver i Nav.

## Ønsket resultat

- undersøke om instruksjonsfiler gjør cplt bedre i DS-oppgaver
- mulighet: undersøke om tokenbruk øker eller minker med instruksjonsfiler
- teste instruksjoner med en konkret visualiseringsoppgave, feks på teamkatalogdata fra BigQuery
- hvis vi er positive: samle et par forslag og ha action points for videre arbeid

> Testing er en viktig del av oppgaven. Instruksjonene skal ikke bare se gode ut i Markdown, men gi et bedre resultat når vi bruker cplt.

> todo: formulere noe rundt tokenbruk

## Agenda

- **09:00:** Introduksjon med HØRA
- **09:05:** Kjapt om cplt
- **09:10:** Hva er instruksjonsfiler og hvorfor?
- **09:15:** Gruppeinndeling og oppstart i Peisestua
- **10:30:** Erfaringsdeling i Gnisten
- **10:45:** Veien videre med instruksjonsfiler
- **10:50:** Tilbakemeldinger på sesjonen

---

- **11:00:** Lunsj i kantina
- **11:50:** Avreise til hemmelig bedriftsbesøk
- **12:30:** Bedriftsbesøket starter


# Kort om cplt

AI-agenter skal alltid kjøre isolert på Nav-utstyr.
Bruk cplt som standard, også når agentarbeidet er personlig.
I knast er cplt ikke mulig, så vi må jobbe på aggregerte tall eller syntetiske datasett.
[Her er noe mer informasjon om tilpassninger til Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/overview).
Husk også at [min-copilot.ansatt.nav.no](https://min-copilot.ansatt.nav.no/praksis) gir mye informasjon om Copilot i Nav, men dette er ikke alltid relevant for DS-hverdagen.


## nav-pilot

...
- nav-pilot (https://min-copilot.ansatt.nav.no/nav-pilot) kjenner Nav sin arkitektur, men mest for utviklere


## Instruksjonsfiler

Instruksjonsfiler er ekstra kontekst til cplt om spesifikke filtyper.
Konteksten skal gjøre at cplt svarer bedre og spytter ut kode tilpasset repoet eller din personlige stil, og at den bruker riktige biblioteker og metoder.
Instruksjonsfiler kan ligge **(1) i et repo** og **(2) i din egen hjemmemappe**.

1. I et repo: `repo/.github/copilot-instructions.md` og `repo/.github/instructions/*.instructions.md`
2. I din egen hjemmemappe: `~/.copilot/copilot-instructions.md`

> F.eks. kan du fortelle cplt at vi alltid bruker **uv** og aldri **pip**.

Bruk `applyTo` for å begrense hvilke filer instruksjonen gjelder for:

```
applyTo: "**" → lastes alltid (bruk sparsomt)
applyTo: "**/*.py" → lastes bare for Python-filer
applyTo: "**/dbt/models/**/*.sql" → lastes bare for dbt-modeller
```

Du sjekker hvilke instruksjoner som er tilgjengelige i cplt med `/instructions`

## Annet

- skills er mer rettet mot spesifikke handlinger, feks java-to-kotlin og kanskje typ maskere-små-tall
- MCP er ...


# Workshop på blåtur

- Bruk cplt til å løse en konkret oppgave, først uten instruksjonsfiler, deretter med instruksjonsfiler.
- Forslag til oppgave
    - Bruk enten egne data og en egen oppgave, med da må alle i gruppa ha tilgang, feks ved å ha åpne på BigQuery
    - Alternativt: visualiser noe fra teamkatalogen i Quarto
        - enten `pensjon-saksbehandli-prod-1f83.teamkatalogen_historikk.personer_med_tilhorighet`
        - eller tabellene på `org-prod-1016.teamkatalogen_federated_query_updated_dataset.*`
- legg instruksjonene under følgende sti i repoet:
    - `gruppe-navn/.github/copilot-instructions.md` # Instruksjoner som gjelder for hele gruppeprosjektet
    - `gruppe-navn/.github/instructions/python.instructions.md` # Instruksjoner for pyhton
    - `gruppe-navn/.github/instructions/sql.instructions.md` # Instruksjoner for sql
    - `gruppe-navn/.github/instructions/<andre-filtyper>.instructions.md` # Instruksjoner for andre filtyper


## Arbeidsform

- Oppgave: visualiser noe fra teamkatalogen, 
- Vi arbeider i grupper på 3 til 5 personer
- Hver gruppe arbeider i sin egen mappe i repoet
- Vi mob-programmerer og bytter på hvem som skriver hvert 15. minutt, da får alle prøvd cplt
- Gruppene committer og pusher forslagene sine til repoet, og dersom dere holder dere i mappa unngår vi merge-konflikter

## Kom i gang

0. Anbefalt: Installer anbefalte VSCode-extensions med `cmd+shift+p` → `Extensions: Show Recommended Extensions` → `Install All`
1. `just` i terminalen: hvis feil, så installer **just**, feks med `brew install just` på Mac
2. `just bootstrap`: installer alt for denne workshopen med
3. `just init <gruppe-navn>`: Opprett gruppens mappe
    - dette oppretter en mappe med et ferdig skjelett, se justfile for detaljer
4. `cd <gruppe-navn>` og så `cplt -d .`: starter cplt i gruppemappen
    - sjekk at det står `Project: .../cplt-ds-instruksjoner/<gruppe-navn>` i cplt
    - verifiser at instruksjonsfilene lastes inn med `/instructions` i cplt

> `-d .` forteller cplt at prosjektmappen er *her* — ikke git-roten. Da finner den instruksjonene i `gruppe-navn/.github/` og gruppen jobber isolert fra de andre gruppene.

### 4. Løs oppgaven

Se `eksempeloppgave.md` i gruppemappen for beskrivelse og BigQuery-tabellnavn.
