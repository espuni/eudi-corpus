#!/usr/bin/env python3
"""Extrae del inventario eidas-references-search-engine los datos que usa el sitio.

Inventario: https://github.com/peppelinux/eidas-references-search-engine
(Giuseppe De Marco, Apache-2.0). Solo se leen `manifest.yaml` y
`report/references-graph.json` de un clon local fijado a un commit; no se
copia texto de ninguna norma.

Escribe `data/inventario.json` con:
- los actos legales (CELEX, ELI, objeto, grupo);
- las normas que esos actos citan directamente (organismo, versión, URL);
- las citas acto → norma.

El hook de MkDocs (`hooks/corpus.py`) genera con eso las páginas de actos y
referencias del sitio.

Uso: python3 -I scripts/importar_inventario.py <ruta-al-clon> <commit>
"""
import json
import pathlib
import sys

import yaml

# Actos de la cartera; el resto del manifiesto son servicios de confianza.
CARTERA = {
    "2024-2977", "2024-2979", "2024-2980", "2024-2981", "2024-2982",
    "2025-846", "2025-847", "2025-848", "2025-849",
    "2026-798", "2026-1730", "2026-1731",
}
# Prefijo del id del grafo → organismo, tal como lo agrupa el sitio.
ORGANISMOS = {"ETSI": "ETSI", "IETF": "IETF", "ISO-IEC": "ISO/IEC", "OpenID": "OpenID",
              "W3C": "W3C", "CEN": "CEN", "ITU-T": "ITU-T", "IEEE": "IEEE"}
# Errores de extracción conocidos del inventario (commit 300f644): ids mal
# partidos que duplican una norma existente.
CORRECCIONES = {
    "ETSI EN 3191 22-1 V1.3.1": "ETSI EN 319 122-1 V1.3.1",
    "ETSI EN 319403-1 V2.3.1": "ETSI EN 319 403-1 V2.3.1",
}


def nombre_acto(kind, aid):
    if kind == "regulation":
        return "Reglamento (UE) 910/2014 (eIDAS), texto consolidado"
    año, num = aid.split("-")
    tipo = "Decisión de Ejecución" if kind == "implementing_decision" else "Reglamento de Ejecución"
    return f"{tipo} (UE) {año}/{num}"


def designacion(node_id, body):
    """«ETSI TS 119 602 V1.1.1» → «TS 119 602»; «IETF RFC 7519» → «RFC 7519»."""
    resto = node_id.split(" ", 1)[1] if " " in node_id else node_id
    partes = resto.split(" ")
    if partes and partes[-1].startswith("V") and partes[-1][1:2].isdigit():
        partes = partes[:-1]
    return " ".join(partes)


def main(clon, commit):
    clon = pathlib.Path(clon)
    raiz = pathlib.Path(__file__).resolve().parent.parent
    manifest = yaml.safe_load((clon / "manifest.yaml").read_text())
    g = json.loads((clon / "report/references-graph.json").read_text())
    nodos = {n["id"]: n for n in g["nodes"]}

    actos = []
    for kind, clave in (("regulation", "regulation"),
                        ("implementing_regulation", "implementing_acts"),
                        ("implementing_decision", "implementing_decisions")):
        for a in manifest.get(clave, []):
            aid = str(a["id"])
            actos.append({
                "id": "eidas" if kind == "regulation" else aid,
                "nombre": nombre_acto(kind, aid),
                "objeto": a.get("title", ""),
                "celex": a.get("celex", ""),
                "eli": (a.get("eli") or "").replace("http://data.europa.eu", "https://data.europa.eu"),
                "grupo": "marco" if kind == "regulation" else ("cartera" if aid in CARTERA else "confianza"),
                "_grafo": f"legal:{aid}",
            })

    citas, refs = [], {}
    for e in g["edges"]:
        if e["kind"] != "cites":
            continue
        acto = next((a for a in actos if a["_grafo"] == e["from"]), None)
        rid = CORRECCIONES.get(e["to"], e["to"])
        n = nodos.get(rid)
        if not acto or not n:
            continue
        body = n.get("body", "?")
        if body not in ORGANISMOS:
            continue
        refs.setdefault(rid, {
            "id": rid,
            "organismo": ORGANISMOS[body],
            "designacion": designacion(rid, body),
            "version": n.get("version") or "",
            "titulo": n.get("title") or "",
            "url": n.get("download_url") or "",
        })
        citas.append({"acto": acto["id"], "ref": rid})

    for a in actos:
        del a["_grafo"]
    salida = {
        "fuente": "https://github.com/peppelinux/eidas-references-search-engine",
        "commit": commit,
        "grafo_generado": g["generated_at"][:10],
        "actos": actos,
        "referencias": sorted(refs.values(), key=lambda r: (r["organismo"], r["designacion"])),
        "citas": sorted({(c["acto"], c["ref"]) for c in citas}),
    }
    salida["citas"] = [{"acto": a, "ref": r} for a, r in salida["citas"]]
    (raiz / "data/inventario.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
