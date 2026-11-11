"""Costruisce il Pensatoio dai sorgenti.

    python3 script/costruisci.py                 # rigenera index.html, il sito
    python3 script/costruisci.py --claude FILE   # scrive anche FILE, la versione per la pagina privata su Claude

Il sito usa i font della cartella fonts/ e non chiede nulla a server esterni.
La versione per Claude carica i font da Google, come la pagina privata pubblicata finora.
"""
import argparse
import html
import json
import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
MODELLO = RADICE / "sorgenti" / "pagina.html"
ARCHIVIO = RADICE / "sorgenti" / "archivio.json"
SITO = RADICE / "index.html"

TITOLO = "Giordano Margotti · Pensatoio"
DESCRIZIONE = "Think slow, grow wise. Articoli e concetti di Giordano Margotti, ordinati per topic e insight."
ICONA = ("data:image/svg+xml,"
         "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%231f43a3'/%3E"
         "%3Cpath d='M22 50V14h12.5c8 0 13 4.4 13 11.3S42.5 36.6 34.5 36.6H29V50z M29 30.6h5c4 0 6.3-2 6.3-5.3S38 20 34 20h-5z' "
         "fill='white' fill-rule='evenodd'/%3E%3C/svg%3E")

# I file "standard" dei font variabili contengono tutti gli assi (Archivo: peso e larghezza; Source Serif 4: peso e dimensione ottica)
FONT = [
    ("Archivo", "normal", "100 900", "62% 125%", "archivo-latin-standard-normal.woff2"),
    ("Source Serif 4", "normal", "200 900", None, "source-serif-4-latin-standard-normal.woff2"),
    ("Source Serif 4", "italic", "200 900", None, "source-serif-4-latin-standard-italic.woff2"),
    ("IBM Plex Mono", "normal", "400", None, "ibm-plex-mono-latin-400-normal.woff2"),
    ("IBM Plex Mono", "normal", "500", None, "ibm-plex-mono-latin-500-normal.woff2"),
]
PRECARICA = ["archivo-latin-standard-normal.woff2", "source-serif-4-latin-standard-normal.woff2"]


def pagina_completa():
    """Il modello con l'archivio inserito al posto del segnaposto: è la pagina pubblicata su Claude."""
    modello = MODELLO.read_text(encoding="utf-8")
    assert modello.count("__ARCHIVIO__") == 1, "il segnaposto __ARCHIVIO__ deve comparire una sola volta"
    archivio = json.loads(ARCHIVIO.read_text(encoding="utf-8"))
    ids = [s["id"] for s in archivio["schede"]]
    assert len(ids) == len(set(ids)), "id delle schede ripetuti"
    for s in archivio["schede"]:
        assert s["argomento"] in archivio["argomenti"], f"topic sconosciuto in {s['id']}"
        for chiave in re.findall(r'data-grafico="([^"]+)"', s.get("testo", "")):
            assert chiave in s.get("grafici", {}), f"figura {chiave} mancante in {s['id']}"
    dati = json.dumps(archivio, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return modello.replace("__ARCHIVIO__", dati), archivio


def sito(pagina):
    """Versione autonoma per il web: testata con titolo, descrizione e icona, font locali."""
    i = pagina.index('<div id="pensatoio">')
    testa, corpo = pagina[:i], pagina[i:]
    stile = re.search(r'<style id="stile">.*?</style>', testa, re.S).group(0)
    regole = []
    for famiglia, stile_font, peso, larghezza, file in FONT:
        assert (RADICE / "fonts" / file).exists(), f"manca fonts/{file}"
        regole.append(
            "@font-face{"
            f'font-family:"{famiglia}";font-style:{stile_font};font-weight:{peso};'
            + (f"font-stretch:{larghezza};" if larghezza else "")
            + f'font-display:swap;src:url("fonts/{file}") format("woff2");}}'
        )
    righe = [
        "<!doctype html>",
        '<html lang="it">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
        f"<title>{html.escape(TITOLO)}</title>",
        f'<meta name="description" content="{html.escape(DESCRIZIONE)}">',
        f'<meta property="og:title" content="{html.escape(TITOLO)}">',
        f'<meta property="og:description" content="{html.escape(DESCRIZIONE)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:locale" content="it_IT">',
        f'<link rel="icon" href="{ICONA}">',
        *[f'<link rel="preload" href="fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in PRECARICA],
        '<style id="font-locali">',
        "/* Font della cartella fonts/ (SIL Open Font License 1.1): Archivo, Source Serif 4, IBM Plex Mono */",
        *regole,
        "</style>",
        stile,
        "</head>",
        "<body>",
    ]
    documento = "\n".join(righe) + "\n" + corpo.rstrip() + "\n</body>\n</html>\n"
    for esterno in ("googleapis", "gstatic", "claude:viewport"):
        assert esterno not in documento, f"riferimento esterno rimasto: {esterno}"
    return documento


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claude", type=pathlib.Path, help="scrive anche la versione per la pagina privata su Claude")
    args = ap.parse_args()
    pagina, archivio = pagina_completa()
    documento = sito(pagina)
    SITO.write_text(documento, encoding="utf-8")
    print(f"index.html: {len(documento.encode('utf-8')) / 1024:.0f} KB, {len(archivio['schede'])} schede")
    if args.claude:
        args.claude.write_text(pagina, encoding="utf-8")
        print(f"{args.claude}: {len(pagina.encode('utf-8')) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
