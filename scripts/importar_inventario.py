#!/usr/bin/env python3
"""Genera tablas del corpus a partir del inventario eidas-references-search-engine.

Inventario: https://github.com/peppelinux/eidas-references-search-engine
(Giuseppe De Marco, Apache-2.0). Solo se leen `manifest.yaml` y
`report/references-graph.json` de un clon local fijado a un commit; no se
copia texto de ninguna norma.

Uso: python3 -I scripts/importar_inventario.py <ruta-al-clon> <commit>
Escribe legal/actos-inventario.md y legal/matriz-actos-normas.md.
"""
import collections
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
# Organismos que se listan por nombre en la matriz.
RELEVANTES = {"ETSI", "OpenID", "W3C", "ARF", "CEN"}
CABECERA_TABLA = ("| Acto | Objeto (según el inventario) | CELEX | Enlace | Verificado en EUR-Lex |\n"
                  "|---|---|---|---|---|\n")


def numero(act_id):
    año, num = act_id.split("-")
    return f"{año}/{num}"


def nombre_acto(kind, aid):
    if kind == "regulation":
        return "Reglamento (UE) 910/2014, texto consolidado"
    tipo = "Decisión de Ejecución" if kind == "implementing_decision" else "Reglamento de Ejecución"
    return f"{tipo} (UE) {numero(aid)}"


def main(clon, commit):
    clon = pathlib.Path(clon)
    raiz = pathlib.Path(__file__).resolve().parent.parent
    manifest = yaml.safe_load((clon / "manifest.yaml").read_text())
    g = json.loads((clon / "report/references-graph.json").read_text())

    actos = ([("regulation", a) for a in manifest.get("regulation", [])]
             + [("implementing_regulation", a) for a in manifest.get("implementing_acts", [])]
             + [("implementing_decision", a) for a in manifest.get("implementing_decisions", [])])

    cab = (f"<!-- GENERADO por scripts/importar_inventario.py desde "
           f"eidas-references-search-engine@{commit[:7]} "
           f"(grafo generado {g['generated_at'][:10]}). No editar a mano. -->\n")

    # --- Lista de actos ---
    filas = {"marco": [], "cartera": [], "confianza": []}
    for kind, a in actos:
        aid = str(a["id"])
        grupo = "marco" if kind == "regulation" else ("cartera" if aid in CARTERA else "confianza")
        eli = (a.get("eli") or "").replace("http://data.europa.eu", "https://data.europa.eu")
        filas[grupo].append(
            f"| {nombre_acto(kind, aid)} | {a.get('title', '')} | {a.get('celex', '')} | [ELI]({eli}) | — |")

    texto = [cab, "# Actos del inventario\n",
             "Actos que recoge el inventario. Objeto y metadatos son los del inventario:\n"
             "cotejar cada fila con EUR-Lex antes de citarla. El tracker editable, con\n"
             "fechas de aplicación y modificaciones, es [`actos.md`](actos.md).\n"]
    for titulo, clave in (("Marco", "marco"),
                          ("Cartera europea de identidad digital", "cartera"),
                          ("Servicios de confianza y otros", "confianza")):
        texto += [f"## {titulo}\n", CABECERA_TABLA + "\n".join(filas[clave]) + "\n"]
    (raiz / "legal/actos-inventario.md").write_text("\n".join(texto))

    # --- Matriz acto -> normas citadas ---
    nodos = {n["id"]: n for n in g["nodes"]}
    citas = collections.defaultdict(set)
    for e in g["edges"]:
        if e["kind"] == "cites":
            citas[e["from"]].add(e["to"])

    m = [cab, "# Matriz acto → normas citadas\n",
         "Qué normas técnicas cita **el texto** de cada acto, según la extracción\n"
         "automática del inventario. Una norma ausente puede llegar por otra vía (ARF,\n"
         "especificaciones técnicas de la Comisión) sin que el acto la cite: por\n"
         "ejemplo, ningún acto cita ETSI TS 119 602 (LoTE). Los actos sin citas\n"
         "detectadas no aparecen.\n",
         "| Acto | ETSI, OpenID, W3C, CEN | IETF | ISO/IEC | Otros |",
         "|---|---|---|---|---|"]
    for kind, a in actos:
        aid = str(a["id"])
        objetivos = citas.get(f"legal:{aid}")
        if not objetivos:
            continue
        por = collections.defaultdict(list)
        for t in sorted(objetivos):
            body = nodos.get(t, {}).get("body", "?")
            etiqueta = t.split(" ", 1)[1] if " " in t else t
            por["rel" if body in RELEVANTES else body].append(etiqueta)
        otros = [x for b, v in por.items() if b not in ("rel", "IETF", "ISO-IEC") for x in v]
        nombre = "eIDAS consolidado" if kind == "regulation" else numero(aid)
        m.append(f"| {nombre} | {'; '.join(por['rel'])} | {'; '.join(por['IETF'])} | "
                 f"{'; '.join(por['ISO-IEC'])} | {'; '.join(otros)} |")
    (raiz / "legal/matriz-actos-normas.md").write_text("\n".join(m) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
