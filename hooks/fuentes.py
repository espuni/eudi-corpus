"""Seguimiento de las fuentes primarias del corpus.

Lee `data/fuentes.yml` y calcula, sin red:

- el estado de revisión de cada fuente (al día, vence pronto, vencida, sin
  revisar), a partir de `revisado` y `periodicidad`;
- el grafo de relaciones entre fuentes: las de `relaciones` más las citas
  acto → norma del inventario de De Marco;
- el impacto de un cambio: qué otras fuentes dependen, directa o
  indirectamente, de cada una.

Lo usan el hook de MkDocs (`corpus.py`, que genera las páginas «Fuentes») y
`scripts/vigilar_fuentes.py` (la revisión periódica, que sí usa la red).
No importa nada de MkDocs para que el script pueda usarlo solo.
"""

from __future__ import annotations

import datetime as _dt
import json
import pathlib
import re
from collections import defaultdict

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent

TIPOS = [
    ("acto", "Legislación UE"), ("arf", "ARF y Comisión"), ("etsi", "ETSI"),
    ("openid", "OpenID Foundation"), ("ietf", "IETF"), ("w3c", "W3C"), ("iso", "ISO/IEC"),
    ("av", "Verificación de edad"), ("herramienta", "Herramientas"),
]
RELACIONES = {
    # tipo: (verbo en el grafo, quién depende de quién)
    "modifica": "modifica",      # A modifica B: si cambia A, cambia el texto vigente de B
    "desarrolla": "desarrolla",  # A desarrolla B: A depende de B
    "cita": "cita",              # A cita B como norma de referencia
    "perfila": "perfila",        # A restringe o concreta B
    "usa": "usa",                # A se apoya en B
}
METODOS = {"git", "eurlex", "manual"}
PRONTO_MAX = 30  # días; para periodicidades cortas, una cuarta parte

# estado → (texto, tono de la píldora, glifo, orden)
ESTADOS = {
    "vencida": ("Revisión vencida", "alert", "▲", 0),
    "sin-revisar": ("Sin revisar", "neutral", "○", 1),
    "pronto": ("Vence pronto", "pending", "◐", 2),
    "al-dia": ("Al día", "verify", "●", 3),
}


class ErrorFuentes(ValueError):
    pass


def _fecha(valor):
    if valor in (None, ""):
        return None
    if isinstance(valor, _dt.date):
        return valor
    return _dt.date.fromisoformat(str(valor))


def cargar(raiz: pathlib.Path = RAIZ) -> list[dict]:
    """Lee y valida el registro. Un error de datos para el build."""
    datos = yaml.safe_load((raiz / "data/fuentes.yml").read_text(encoding="utf-8"))
    fuentes = datos["fuentes"]
    ids = [f["id"] for f in fuentes]
    repetidos = {i for i in ids if ids.count(i) > 1}
    if repetidos:
        raise ErrorFuentes(f"fuentes.yml: ids repetidos: {sorted(repetidos)}")
    conocidos = set(ids)
    tipos = {t for t, _ in TIPOS}
    for f in fuentes:
        donde = f"fuentes.yml, {f['id']}"
        if f.get("tipo") not in tipos:
            raise ErrorFuentes(f"{donde}: tipo desconocido {f.get('tipo')!r}")
        if not isinstance(f.get("periodicidad"), int) or f["periodicidad"] <= 0:
            raise ErrorFuentes(f"{donde}: periodicidad debe ser un número de días")
        v = f.get("vigilar") or {}
        if v.get("metodo") not in METODOS:
            raise ErrorFuentes(f"{donde}: vigilar.metodo debe ser uno de {sorted(METODOS)}")
        if v["metodo"] == "git" and not v.get("repo"):
            raise ErrorFuentes(f"{donde}: vigilar.repo es obligatorio con metodo git")
        if v["metodo"] == "eurlex" and not v.get("celex"):
            raise ErrorFuentes(f"{donde}: vigilar.celex es obligatorio con metodo eurlex")
        if v["metodo"] == "manual" and not v.get("donde"):
            raise ErrorFuentes(f"{donde}: vigilar.donde es obligatorio con metodo manual")
        for r in f.get("relaciones") or []:
            if r.get("tipo") not in RELACIONES:
                raise ErrorFuentes(f"{donde}: relación desconocida {r.get('tipo')!r}")
            if r.get("a") not in conocidos:
                raise ErrorFuentes(f"{donde}: la relación apunta a {r.get('a')!r}, que no existe")
        try:
            f["revisado"] = _fecha(f.get("revisado"))
        except ValueError as e:
            raise ErrorFuentes(f"{donde}: revisado no es una fecha: {e}") from e
    return fuentes


def estado(f: dict, hoy: _dt.date) -> tuple[str, _dt.date | None]:
    """Clave de estado y fecha de la próxima revisión."""
    if not f.get("revisado"):
        return "sin-revisar", None
    proxima = f["revisado"] + _dt.timedelta(days=f["periodicidad"])
    if proxima < hoy:
        return "vencida", proxima
    if (proxima - hoy).days <= min(PRONTO_MAX, f["periodicidad"] // 4):
        return "pronto", proxima
    return "al-dia", proxima


def aristas(fuentes: list[dict], raiz: pathlib.Path = RAIZ) -> list[dict]:
    """Relaciones declaradas más las citas acto → norma del inventario."""
    por_ref = {f["ref"]: f["id"] for f in fuentes if f.get("ref")}
    salida, vistas = [], set()
    for f in fuentes:
        for r in f.get("relaciones") or []:
            clave = (f["id"], r["a"], r["tipo"])
            if clave not in vistas:
                vistas.add(clave)
                salida.append({"de": f["id"], "a": r["a"], "tipo": r["tipo"], "auto": False})
    inv = json.loads((raiz / "data/inventario.json").read_text(encoding="utf-8"))
    ya = {(a["de"], a["a"]) for a in salida}
    for c in inv["citas"]:
        de, a = por_ref.get(f"acto:{c['acto']}"), por_ref.get(c["ref"])
        if de and a and de != a and (de, a) not in ya:
            ya.add((de, a))
            salida.append({"de": de, "a": a, "tipo": "cita", "auto": True})
    return salida


def dependencias(aristas_: list[dict]) -> tuple[dict[str, set], dict[str, set]]:
    """Qué hay que revisar si cambia x, en dos grupos.

    - por_texto[x]: fuentes cuyo texto vigente cambia con x (x las modifica);
    - por_uso[x]: fuentes que citan, perfilan, usan o desarrollan x.
    """
    por_texto, por_uso = defaultdict(set), defaultdict(set)
    for a in aristas_:
        if a["tipo"] == "modifica":
            por_texto[a["de"]].add(a["a"])
        else:
            por_uso[a["a"]].add(a["de"])
    return por_texto, por_uso


def impacto(aristas_: list[dict]) -> dict[str, set]:
    """Fuentes afectadas, directa o indirectamente, si cambia cada una.

    «modifica» solo cuenta en el primer salto: si cambia OpenID4VP, hay que
    revisar 2026/1731, que la cita, pero no cambia el texto de los actos que
    2026/1731 modifica. Si cambia 2026/1731, sí.
    """
    por_texto, por_uso = dependencias(aristas_)
    total = {}
    for x in set(por_texto) | set(por_uso):
        vistos = set(por_texto.get(x, ())) | set(por_uso.get(x, ()))
        pila = list(vistos)
        while pila:
            for y in por_uso.get(pila.pop(), ()):
                if y not in vistos and y != x:
                    vistos.add(y)
                    pila.append(y)
        vistos.discard(x)
        total[x] = vistos
    return total


def url_vigilar(f: dict) -> tuple[str, str]:
    """(texto, URL) de dónde mirar si la fuente ha cambiado."""
    v = f["vigilar"]
    if v["metodo"] == "git":
        base = v.get("base")
        if base:
            return (f"commits desde {base[:7] if len(base) == 40 else base}",
                    f"https://github.com/{v['repo']}/compare/{base}...HEAD")
        return ("commits del repositorio", f"https://github.com/{v['repo']}/commits")
    if v["metodo"] == "eurlex":
        return ("relaciones y consolidaciones en EUR-Lex",
                f"https://eur-lex.europa.eu/legal-content/ES/ALL/?uri=CELEX:{v['celex']}")
    return (v.get("que") or "revisar a mano", v["donde"])


def descripcion_vigilar(f: dict) -> str:
    v = f["vigilar"]
    texto, url = url_vigilar(f)
    if v["metodo"] == "git":
        extra = f"; etiquetas `{v['etiquetas']}`" if v.get("etiquetas") else ""
        rutas = f" en `{', '.join(v['rutas'])}`" if v.get("rutas") else ""
        return (f"Automático: [{texto}]({url}){rutas}{extra} en "
                f"[`{v['repo']}`](https://github.com/{v['repo']})")
    if v["metodo"] == "eurlex":
        conocidos = v.get("conocidos") or []
        extra = f" Modificaciones ya incorporadas: {', '.join(conocidos)}." if conocidos else ""
        return f"Manual: [{texto}]({url}), CELEX `{v['celex']}`.{extra}"
    return f"Manual: [{texto}]({url})"


# ----------------------------------------------------------------- páginas

def _nodo(i: str) -> str:
    return "n_" + re.sub(r"\W", "_", i)


def _etiqueta(f: dict) -> str:
    if f.get("corto"):
        return f["corto"].replace('"', "'")
    corta = f["nombre"].split(" · ")[0]
    corta = re.sub(r"\s*\((?:borrador|RFC \d+)[^)]*\)", "", corta)
    corta = corta.replace('"', "'")
    if len(corta) > 34:
        corta = corta[:32].rstrip() + "…"
    return corta


def mermaid(fuentes: list[dict], aristas_: list[dict], hoy: _dt.date, url_base: str) -> str:
    """Diagrama de las fuentes. Las aristas «desarrolla» hacia eIDAS se omiten:
    las comparten todos los actos de ejecución y tapan el resto."""
    por_tipo = defaultdict(list)
    for f in fuentes:
        por_tipo[f["tipo"]].append(f)
    lineas = ["flowchart LR"]
    for clave, titulo in TIPOS:
        if not por_tipo[clave]:
            continue
        lineas.append(f'  subgraph g_{clave}["{titulo}"]')
        lineas.append("    direction TB")
        for f in por_tipo[clave]:
            lineas.append(f'    {_nodo(f["id"])}["{_etiqueta(f)}"]')
        lineas.append("  end")
    estilos = []
    n = 0
    for a in aristas_:
        if a["tipo"] == "desarrolla" and a["a"] == "eidas":
            continue
        de, para = _nodo(a["de"]), _nodo(a["a"])
        if a["tipo"] == "modifica":
            lineas.append(f"  {de} ==>|modifica| {para}")
            estilos.append(f"  linkStyle {n} stroke:#A93C0A,stroke-width:3px")
        elif a["tipo"] == "perfila":
            lineas.append(f"  {de} -.->|perfila| {para}")
            estilos.append(f"  linkStyle {n} stroke:#1F5FBF,stroke-width:2px")
        elif a["tipo"] == "usa":
            lineas.append(f"  {de} -.-> {para}")
            estilos.append(f"  linkStyle {n} stroke:#5B6470,stroke-width:1.5px")
        else:  # cita, desarrolla
            lineas.append(f"  {de} --> {para}")
            estilos.append(f"  linkStyle {n} stroke:#3E4753,stroke-width:1.5px")
        n += 1
    lineas += estilos
    colores = {
        "vencida": "fill:#FBE7DA,stroke:#A93C0A,color:#16202B",
        "sin-revisar": "fill:#E7E9EC,stroke:#4A5360,color:#16202B,stroke-dasharray:4 3",
        "pronto": "fill:#FAEFCF,stroke:#7D5800,color:#16202B",
        "al-dia": "fill:#E0F0E6,stroke:#1B6544,color:#16202B",
    }
    for clave, estilo in colores.items():
        lineas.append(f"  classDef {clave.replace('-', '_')} {estilo}")
    for f in fuentes:
        lineas.append(f"  class {_nodo(f['id'])} {estado(f, hoy)[0].replace('-', '_')}")
        lineas.append(f'  click {_nodo(f["id"])} "{url_base}fuentes/#{f["id"]}" "Ver la fuente"')
    return "\n".join(lineas)


def generar_paginas(fuentes, refs, ref_en, fichas_por_uri, hoy, url_base, pill, aviso) -> dict[str, str]:
    """Páginas «Fuentes»: seguimiento (fuentes/index.md) y grafo (fuentes/grafo.md)."""
    aristas_ = aristas(fuentes)
    imp = impacto(aristas_)
    por_id = {f["id"]: f for f in fuentes}
    usa_de = defaultdict(list)       # de → [(a, tipo)]
    for a in aristas_:
        usa_de[a["de"]].append((a["a"], a["tipo"]))

    def enlace_fuente(i):
        return f"[{_etiqueta(por_id[i])}](#{i})"

    def fichas_de(f):
        ids = []
        for uri in sorted(ref_en.get(f.get("ref"), ())):
            info = fichas_por_uri.get(uri)
            if info:
                ids.append(f"[`{info['meta']['id']}`](../{uri})")
        return ids

    def pildora(f):
        clave, _ = estado(f, hoy)
        texto, tono, glifo, _ = ESTADOS[clave]
        return pill(texto, tono, glifo)

    def fecha(d):
        return d.isoformat() if d else "—"

    cuenta = defaultdict(int)
    for f in fuentes:
        cuenta[estado(f, hoy)[0]] += 1

    pendientes = sorted(
        (f for f in fuentes if estado(f, hoy)[0] != "al-dia"),
        key=lambda f: (ESTADOS[estado(f, hoy)[0]][3], estado(f, hoy)[1] or _dt.date.min, f["id"]))
    filas_pend = []
    for f in pendientes:
        clave, proxima = estado(f, hoy)
        texto, url = url_vigilar(f)
        filas_pend.append(f"| [{f['nombre']}](#{f['id']}) | {pildora(f)} | "
                          f"<span class=\"id\">{fecha(proxima)}</span> | [{texto}]({url}) |")

    bloques = []
    for clave, titulo in TIPOS:
        grupo = [f for f in fuentes if f["tipo"] == clave]
        if not grupo:
            continue
        bloques.append(f"## {titulo}\n")
        for f in grupo:
            _, proxima = estado(f, hoy)
            r = refs.get(f.get("ref") or "")
            url = f.get("url") or (r or {}).get("url")
            doc = f"[abrir]({url})" if url else "sin enlace público"
            cat = (f" · [catálogo](../{r['pagina']}#{r['ancla']})" if r else "")
            datos = [
                f"### {f['nombre']} {{ #{f['id']} }}\n",
                f"{pildora(f)} &nbsp; Citada: **{f.get('citada') or 'por fijar'}** · "
                f"revisada: <span class=\"id\">{fecha(f.get('revisado'))}</span> · "
                f"próxima: <span class=\"id\">{fecha(proxima)}</span> · "
                f"cada {f['periodicidad']} días · {doc}{cat}\n",
                f"- **Vigilar:** {descripcion_vigilar(f)}",
            ]
            dep = usa_de.get(f["id"])
            if dep:
                datos.append("- **Relaciones:** " + ", ".join(
                    f"{RELACIONES[t]} {enlace_fuente(a)}" for a, t in sorted(dep, key=lambda x: (x[1], x[0]))))
            afecta = imp.get(f["id"])
            if afecta:
                datos.append(f"- **Si cambia, revisar también ({len(afecta)}):** "
                             + ", ".join(enlace_fuente(i) for i in sorted(afecta)))
            fi = fichas_de(f)
            if fi:
                datos.append("- **Fichas que la citan:** " + ", ".join(fi))
            if f.get("nota"):
                datos.append(f"- **Nota:** {f['nota']}")
            bloques.append("\n".join(datos) + "\n")

    resumen = " · ".join(
        f"{pill(ESTADOS[k][0], ESTADOS[k][1], ESTADOS[k][2])} **{cuenta.get(k, 0)}**"
        for k in ("vencida", "sin-revisar", "pronto", "al-dia"))
    automaticas = sum(1 for f in fuentes if f["vigilar"]["metodo"] == "git")

    seguimiento = "\n".join([
        "# Seguimiento de fuentes\n", aviso,
        f"Las **{len(fuentes)} fuentes primarias** de las que sale lo que afirma el corpus: qué "
        "versión se cita, cuándo se revisó, cuándo toca volver a mirarla, dónde se ve si ha "
        "cambiado y qué hay que revisar si cambia. El registro está en `data/fuentes.yml`; las "
        f"relaciones entre fuentes, en el [grafo](grafo.md).\n",
        f"Estado a <span class=\"id\">{hoy.isoformat()}</span>: {resumen}\n",
        "## Revisar ahora\n",
        "Fuentes con la revisión vencida, que vencen pronto (30 días, o la cuarta parte de su "
        "periodicidad si es más corta) o que nunca se han "
        "revisado contra el texto.\n",
        *(["| Fuente | Estado | Tocaba | Dónde mirar |", "|---|---|---|---|", *filas_pend]
          if filas_pend else ["Nada pendiente."]), "",
        "## Cómo se revisa\n",
        f"1. **Cada mes**, el flujo `vigilar-fuentes` comprueba solo las {automaticas} fuentes que "
        "viven en GitHub (etiquetas nuevas y commits desde la versión citada) y abre o actualiza "
        "un issue `revision-fuentes` con lo detectado y con las revisiones manuales que tocan. "
        "Se puede lanzar a mano desde *Actions*.",
        "2. Para cada fuente del issue, abrir **Dónde mirar** y compararlo con la versión citada.",
        "3. **Si no ha cambiado nada relevante:** poner la fecha de hoy en `revisado`.",
        "4. **Si ha cambiado:** actualizar `citada`, `url` y `base` (o `conocidos`, en un acto), "
        "revisar las **fichas que la citan** y las fuentes de **«si cambia, revisar también»**, y "
        "anotarlo en la ficha. Un acto que modifica a otro se añade como fuente nueva, con su "
        "relación `modifica`.",
        "5. Si avanza el **inventario de De Marco**, reimportarlo: es como aparecen actos y citas "
        "nuevas.\n",
        "Las fuentes de pago (ISO) y las que no tienen un sitio que se pueda comprobar solo (EUR-Lex, "
        "ETSI, erratas de RFC) se revisan a mano, con la periodicidad que marca su entrada.\n",
        *bloques,
    ])

    leyenda = "\n".join([
        "| Trazo | Significa |", "|---|---|",
        "| Grueso, «modifica» | El acto de origen cambia el texto del de destino |",
        "| Continuo | Cita (acto → norma; las del inventario de De Marco se añaden solas) |",
        "| Discontinuo, «perfila» | Restringe o concreta la norma de destino |",
        "| Punteado fino | Se apoya en ella |",
        "", "| Nodo | Estado de revisión |", "|---|---|",
        "| Verde, borde continuo | Al día |",
        "| Ámbar | Vence pronto |",
        "| Rojo claro | Revisión vencida |",
        "| Gris, borde discontinuo | Nunca revisada contra el texto |",
    ])
    filas_imp = []
    for i in sorted(imp, key=lambda x: (-len(imp[x]), x)):
        if imp[i]:
            filas_imp.append(f"| [{por_id[i]['nombre']}](index.md#{i}) | {len(imp[i])} | "
                             + ", ".join(f"[{_etiqueta(por_id[x])}](index.md#{x})" for x in sorted(imp[i]))
                             + " |")
    auto = sum(1 for a in aristas_ if a["auto"])
    grafo = "\n".join([
        "# Grafo de fuentes\n", aviso,
        f"{len(fuentes)} fuentes y {len(aristas_)} relaciones ({auto} sacadas de las citas del "
        "inventario de De Marco). El color de cada nodo es su estado de revisión; un clic lleva a "
        "su ficha de seguimiento. Las relaciones «desarrolla» de los actos de ejecución con eIDAS "
        "no se dibujan, porque las comparten todos.\n",
        "``` mermaid", mermaid(fuentes, aristas_, hoy, url_base), "```\n",
        "## Leyenda\n", leyenda, "",
        "## Impacto de un cambio\n",
        "Qué fuentes quedan afectadas, directa o indirectamente, si cambia cada una. Se ordena por "
        "alcance: lo de arriba es lo que más conviene vigilar.\n",
        "| Si cambia | Fuentes afectadas | Cuáles |", "|---|---|---|", *filas_imp, "",
    ])
    return {"fuentes/index.md": seguimiento, "fuentes/grafo.md": grafo}
