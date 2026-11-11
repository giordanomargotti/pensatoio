# Pensatoio — istruzioni per Claude

Sito statico di Giordano Margotti, pubblicato con GitHub Pages dal ramo `main` (cartella radice): https://giordanomargotti.github.io/pensatoio/. L'autore lo aggiorna solo dalla chat; risposte in italiano.

## Flusso di aggiornamento
1. Modifica `sorgenti/archivio.json` (contenuti) o `sorgenti/pagina.html` (stile, menu, figure). `index.html` non si tocca a mano.
2. `python3 script/costruisci.py --claude build/pensatoio-claude.html` rigenera `index.html` e la versione per la pagina privata su Claude (https://claude.ai/artifact/UiofCAyUkwLjgNkoZBMwMn, slug `e07cfe22-1baf-4f34-9298-024c9ed8fa0d`). La cartella `build/` resta fuori da git.
3. Controlla nel browser: computer (1280 px) e telefono (390 px), tema chiaro e scuro, apertura degli articoli dai menu, nessun errore in console, nessuna richiesta a server esterni.
4. Commit su `main` e push; ripubblica anche la pagina privata su Claude pubblicando `build/pensatoio-claude.html` come `index.html` dell'artifact.

## Regole
- Testata: solo GIORDANO MARGOTTI (su due righe) e "Think slow, grow wise.". Niente scritte superflue, contatori o ricerca. Titolo del sito: "Giordano Margotti · Pensatoio".
- Menu Topic (argomenti, ciascuno con i suoi temi) e Insight (fonti per tipo). Pagina vuota finché non si sceglie; se la scelta porta a una sola scheda l'articolo si apre subito, altrimenti elenco con "Leggi →".
- Articoli del blog e del sito: testo integrale e verbatim (refusi compresi), senza riordino né commenti; niente link all'origine nelle schede (il campo `origini` resta nei dati).
- Immagini degli articoli ridisegnate nello stile della pagina, nel punto del testo dove stavano; immagine originale (data URI) solo se mancano i dati per ridisegnarla. Se l'autore chiede "immagini coerenti": schemi tra un paragrafo e l'altro, senza toccare il testo.
- Navigazione solo con pulsanti: niente link interni con `#` e niente modifiche all'indirizzo (dentro Claude portano fuori dalla pagina). Un `#id` nell'indirizzo apre la scheda all'avvio.

## Dati (`sorgenti/archivio.json`)
`argomenti` (i topic) e `schede`. Ogni scheda: `id`, `titolo`, `data` (AAAA-MM-GG, può essere vuota), `aggiunta`, `argomento`, `temi` (il primo è la voce del menu), `stimoli` (gli insight: tipo, autore, titolo, anno, nota), `origini`, `testo` (HTML; la pagina lo ripulisce), `grafici` (richiamati nel testo con `<figure data-grafico="nome">`).
Tipi di figura: linea, dispersione, quote, istogrammi, flusso, wfa, bitmap, crossover, tabella (anche `testuale`), immagine, ciclo, scala, schema, fasce, filiera, raccomandazione.

## Da fare
- Date mancanti: Customer segmentation in R, Dynamic pricing, Il marketing nell'era dei big data.
- Dominio giordanomargotti.com da collegare (file `CNAME` e record DNS dal registrar).
