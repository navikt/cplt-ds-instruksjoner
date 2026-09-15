---
applyTo: "**/*.qmd"
---

# NAV-identitet i Quarto-fortellinger

Bruk NAVs merkevare for alle Quarto-fortellinger, visualiseringer, tabeller og
egendefinert HTML/CSS. Den kanoniske kildekonfigurasjonen er
[`brand/_brand.yaml`](https://github.com/navikt/komme-i-gang-med-llm/blob/main/brand/_brand.yaml).

Sett Nav-logoen der det passer (mange steder).

Alltid ha akse-titler som er gode 👍. Alltid inkluder en beskrivelse av hva man ser i en figur.

Alltid ha mulighet for dark-mode 😎.

## Typografi og grunnflate

- Bruk `Source Sans 3` for brødtekst, overskrifter og diagrammer. Last den inn
  via Google Fonts når Quarto-temaet eller visualiseringsbiblioteket trenger en
  eksplisitt skrifttype.
- Bruk lys bakgrunn `#ffffff` og mørk forgrunn `#202733` som standard.
- Ved mørk visning skal bakgrunnen være `#0e151f` og teksten `#dfe1e5`.
- Hold flater rolige. Bruk `#ecedef` til diskrete bakgrunner, skillelinjer og
  kodeblokker i lys visning.

## Fargebruk

- Gi farger en betydning. Ikke bruk farge alene for å formidle viktig
  informasjon; behold forklarende etiketter, mønstre eller direkte verdier.
- Bruk én gjennomgående aksentfarge for én serie:
  `accent-600` `#2176D4`, `accent-700` `#0063c1` eller `accent-800` `#005bb6`.
- Bruk semantiske farger bare når dataene representerer tilstanden:
  suksess `#00893c`, informasjon `#457c9d`, advarsel `#ca5000` og fare
  `#e22948`.
- For flere kategorier, bruk denne rekkefølgen og gjenta den konsekvent:
  `#2176D4`, `#b65681`, `#457c9d`, `#ad634a`, `#905bd3`, `#757c00`.
- Bruk NAVs mørke fargevarianter ved mørk bakgrunn: aksent `#4580ca`, suksess
  `#378f53`, informasjon `#5b839c`, advarsel `#c56333` og fare `#de4a50`.
- Bruk magenta `#b65681` som primær merkevarefarge og lenkefarge. Bruk
  `#457c9d` som sekundærfarge og `#ad634a` som tertiærfarge.

## Visualiseringer

- Velg en diagramtype som besvarer ett tydelig spørsmål, og skriv en kort
  forklaring av hva leseren skal se før diagrammet.
- Bruk beskrivende tittel, norske akseetiketter og synlige enheter. Unngå
  legende når serien kan etiketteres direkte.
- Start stolpediagrammer på null og sorter kategorier etter verdien når
  sammenligning er formålet.
- Hent og vis aggregerte data når individnivå ikke er nødvendig. Ikke legg
  personopplysninger i rapporter eller visualiseringer.
- Definer eksplisitt fargepalett og skrifttype i Plotly-figurer. Ikke stol på
  bibliotekets standardfarger.

```python
NAV_KATEGORIER = [
    "#2176D4", "#b65681", "#457c9d",
    "#ad634a", "#905bd3", "#757c00",
]

fig.update_layout(
    font={"family": "Source Sans 3, sans-serif", "color": "#202733"},
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
)
```
