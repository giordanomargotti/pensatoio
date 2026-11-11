# Pensatoio

*Think slow, grow wise.* Articoli e concetti di Giordano Margotti, ordinati per topic e insight.

Sito: https://giordanomargotti.github.io/pensatoio/

## Come si aggiorna

Dalla chat con Claude («Pensatoio: …»). Claude modifica i sorgenti, rigenera `index.html` e fa il commit; GitHub Pages mette online la nuova versione in qualche minuto.

## Contenuto

| Percorso | Cosa contiene |
|---|---|
| `index.html` | il sito, generato: non si modifica a mano |
| `sorgenti/archivio.json` | le schede: testi integrali, insight, dati delle figure |
| `sorgenti/pagina.html` | il modello della pagina (stile, menu, figure) con il segnaposto `__ARCHIVIO__` |
| `script/costruisci.py` | rigenera `index.html`: `python3 script/costruisci.py` |
| `fonts/` | Archivo, Source Serif 4 e IBM Plex Mono, con le licenze (SIL Open Font License 1.1) |
