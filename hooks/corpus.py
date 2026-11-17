"""Hook de MkDocs que convierte el corpus en un sitio navegable.

Hace tres cosas en cada build:

1. Genera páginas que no se editan a mano:
   - `index.md`: el panel (estado de las fichas, revisiones pendientes,
     referencias y tracker legal);
   - `referencias/*.md`: el catálogo de documentos referenciados, una página
     por organismo, con el enlace a cada documento, qué actos lo citan y qué
     fichas del corpus lo mencionan.
2. Enlaza dentro del texto las menciones a documentos del catálogo y a otras
   fichas (la primera de cada una por página, fuera de código y de enlaces).
3. Añade a cada ficha un recuadro con sus metadatos y, al final, las
   referencias que cita y las fichas que la citan.

Datos: `data/inventario.json` (generado por `scripts/importar_inventario.py`)
y `data/referencias.yml` (mantenido a mano).
"""

from __future__ import annotations

import datetime as _dt
import json
import pathlib
import posixpath
import re
from collections import defaultdict

import yaml
from mkdocs.structure.files import File

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HOY = _dt.date.today()
VENTANA_REVISION = _dt.timedelta(days=90)

SECCIONES = [
    ("legal", "Legal"), ("arf", "ARF"), ("protocolos", "Protocolos"),
    ("formatos", "Formatos"), ("confianza", "Confianza y PKI"),
    ("edad", "Verificación de edad"), ("observaciones", "Observaciones"),
    ("criterios", "Criterios"), ("evaluacion", "Evaluación"),
]

# Organismo → (página del catálogo, título de la página, orden).
PAGINAS = {
    "Legislación UE": ("legislacion", "Legislación de la UE", 0),
    "ARF": ("arf", "ARF y especificaciones técnicas de la Comisión", 1),
    "Comisión Europea (TS)": ("arf", "ARF y especificaciones técnicas de la Comisión", 1),
    "Verificación de edad": ("verificacion-edad", "Verificación de edad", 2),
    "ETSI": ("etsi", "ETSI", 3),
    "ISO/IEC": ("iso-iec", "ISO/IEC", 4),
    "IETF": ("ietf", "IETF", 5),
    "OpenID": ("openid", "OpenID Foundation", 6),
    "W3C": ("w3c", "W3C", 7),
    "CEN": ("cen", "CEN", 8),
    "Otros": ("otros", "Otros", 9),
}

GRUPOS_ACTOS = [("marco", "Marco"), ("cartera", "Cartera europea de identidad digital"),
                ("confianza", "Servicios de confianza y otros")]

ID_FICHA = re.compile(r"\b(LEG|ARF|PRO|FMT|CNF|AV|OBS|CRI|EVA)-\d{3}\b")
PROTEGIDO = re.compile(r"`[^`\n]*`|!?\[[^\]\n]*\]\([^)\n]*\)|<[^>\n]+>|https?://[^\s)|]+|\{[^}\n]*\}")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

_estado: dict = {}


# ---------------------------------------------------------------- utilidades

def slug(texto: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "-", texto.lower()).strip("-")
    return s or "ref"


def rel(desde: str, hacia: str) -> str:
    """Enlace relativo entre dos src_uri de MkDocs."""
    return posixpath.relpath(hacia, posixpath.dirname(desde) or ".")


def alias_por_defecto(ref: dict) -> list[str]:
    d = ref["designacion"]
    org = ref["organismo"]
    if org == "ETSI":
        cuerpo = r"\s+".join(map(re.escape, d.split(" ")))
        return [rf"(?:ETSI\s+)?{cuerpo}(?![-\d])(?:\s+V\d+\.\d+\.\d+)?"]
    if org == "IETF" and d.startswith("RFC"):
        return [rf"RFC\s?{d.split()[-1]}(?!\d)"]
    if org == "ISO/IEC":
        num = d.split(" ", 1)[1] if " " in d else d
        num = num.replace("ISO/IEC ", "")
        return [rf"ISO(?:/IEC)?\s+(?:TS\s+)?{re.escape(num)}(?![-\d])(?::\d{{4}})?"]
    if org == "OpenID":
        if "HAIP" in d:
            return [r"(?<![\w-])HAIP(?![\w-])"]
        return [rf"(?<![\w-]){re.escape(d)}(?![\w-])"]
    if org == "IETF" and d.startswith("SD-JWT"):
        return [rf"(?<![\w-]){re.escape(d)}(?![\w-])"]
    return []


def cargar_referencias() -> tuple[dict, list]:
    inv = json.loads((RAIZ / "data/inventario.json").read_text())
    manual = yaml.safe_load((RAIZ / "data/referencias.yml").read_text())["referencias"]
    refs: dict[str, dict] = {}
    for a in inv["actos"]:
        num = "910/2014" if a["id"] == "eidas" else a["id"].replace("-", "/")
        refs[f"acto:{a['id']}"] = {
            "id": f"acto:{a['id']}", "organismo": "Legislación UE", "designacion": a["nombre"],
            "titulo": a["objeto"], "version": a["celex"], "url": a["eli"], "grupo": a["grupo"],
            "alias": [rf"(?<![\d/]){re.escape(num)}(?!\d)"], "acto": True,
        }
    for r in inv["referencias"]:
        refs[r["id"]] = dict(r)
    for r in manual:
        refs[r["id"]] = {**refs.get(r["id"], {}), **r}
    for r in refs.values():
        if "alias" not in r or not r["alias"]:
            r["alias"] = r.get("alias") or alias_por_defecto(r)
        pagina, _, _ = PAGINAS.get(r["organismo"], PAGINAS["Otros"])
        r["pagina"] = f"referencias/{pagina}.md"
    # Anclas únicas por página.
    usados: dict[str, set] = defaultdict(set)
    for r in sorted(refs.values(), key=lambda r: r["id"]):
        base = slug(r["designacion"])
        ancla = base if base not in usados[r["pagina"]] else slug(f"{r['designacion']} {r.get('version', '')}")
        usados[r["pagina"]].add(ancla)
        r["ancla"] = ancla
    for r in refs.values():
        r["_re"] = [re.compile(a) for a in r["alias"]]
    citas = inv["citas"]
    _estado["inventario"] = {k: inv[k] for k in ("fuente", "commit", "grafo_generado")}
    return refs, citas


def leer_ficha(src: pathlib.Path, src_uri: str) -> dict | None:
    texto = src.read_text(encoding="utf-8")
    m = FRONTMATTER.match(texto)
    meta = {}
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
    cuerpo = texto[m.end():] if m else texto
    h1 = re.search(r"^# (.+)$", cuerpo, re.M)
    return {"src_uri": src_uri, "meta": meta, "cuerpo": cuerpo,
            "titulo": (h1.group(1).strip() if h1 else meta.get("titulo") or src_uri)}


def es_ficha(f: dict) -> bool:
    i = str(f["meta"].get("id", ""))
    return bool(ID_FICHA.fullmatch(i)) and not i.endswith("-000") \
        and not f["src_uri"].startswith("plantillas/")


def trozos_texto(markdown: str):
    """Itera (es_texto, trozo): separa bloques de código cercados."""
    partes = re.split(r"(^```.*?^```[^\n]*$)", markdown, flags=re.S | re.M)
    for i, p in enumerate(partes):
        yield (i % 2 == 0), p


def menciones(markdown: str, refs: dict, ficha_ids: set) -> tuple[set, set]:
    """Referencias y fichas mencionadas en un texto (fuera de código)."""
    r_vistas, f_vistas = set(), set()
    for es_texto, trozo in trozos_texto(markdown):
        if not es_texto:
            continue
        limpio = PROTEGIDO.sub(" ", trozo)
        for m in ID_FICHA.finditer(limpio):
            if m.group(0) in ficha_ids:
                f_vistas.add(m.group(0))
        for rid, r in refs.items():
            if any(rx.search(limpio) for rx in r["_re"]):
                r_vistas.add(rid)
    return r_vistas, f_vistas


# ------------------------------------------------------------------- eventos

def on_files(files, config):
    docs = pathlib.Path(config["docs_dir"])
    refs, citas = cargar_referencias()
    fichas: dict[str, dict] = {}
    paginas: dict[str, dict] = {}
    for f in files.documentation_pages():
        info = leer_ficha(docs / f.src_uri, f.src_uri)
        paginas[f.src_uri] = info
        if es_ficha(info):
            fichas[str(info["meta"]["id"])] = info
    ids = set(fichas)
    ref_en = defaultdict(set)      # ref → páginas que la mencionan
    ficha_en = defaultdict(set)    # id de ficha → páginas que la mencionan
    for uri, info in paginas.items():
        if uri.startswith("plantillas/"):
            continue
        rv, fv = menciones(info["cuerpo"], refs, ids)
        info["refs"], info["fichas"] = rv, fv
        for r in rv:
            ref_en[r].add(uri)
        for i in fv:
            ficha_en[i].add(uri)
    _estado.update(refs=refs, citas=citas, fichas=fichas, paginas=paginas,
                   ref_en=ref_en, ficha_en=ficha_en, por_uri={i["src_uri"]: i for i in fichas.values()})

    for uri, contenido in generar_catalogo().items():
        files.append(File.generated(config, uri, content=contenido))
    files.append(File.generated(config, "index.md", content=generar_panel()))
    return files


def on_page_markdown(markdown, page, config, files):
    uri = page.file.src_uri
    if uri.startswith("plantillas/"):
        crudo = (pathlib.Path(config["docs_dir"]) / uri).read_text(encoding="utf-8")
        nombre = pathlib.Path(uri).stem
        return (f"# Plantilla: {nombre}\n\nCopiar tal cual y rellenar. "
                f"Ver [el método](../metodo.md).\n\n````markdown\n{crudo}\n````\n")
    if page.file.generated_by:
        return markdown
    info = _estado["paginas"].get(uri)
    propio = str(info["meta"].get("id")) if info and es_ficha(info) else None
    markdown = enlazar(markdown, uri, propio)
    if propio:
        markdown = recuadro(markdown, uri, info) + pie(uri, info, propio)
    return markdown


# ---------------------------------------------------------- enlazado en texto

def enlazar(markdown: str, uri: str, propio: str | None) -> str:
    refs, fichas = _estado["refs"], _estado["fichas"]
    hechos: set = set()
    salida = []
    for es_texto, trozo in trozos_texto(markdown):
        if not es_texto:
            salida.append(trozo)
            continue
        lineas = []
        for linea in trozo.split("\n"):
            if linea.lstrip().startswith("#") or set(linea.strip()) <= set("|-: "):
                lineas.append(linea)
                continue
            lineas.append(enlazar_linea(linea, uri, propio, refs, fichas, hechos))
        salida.append("\n".join(lineas))
    return "".join(salida)


def enlazar_linea(linea, uri, propio, refs, fichas, hechos):
    guardados: list[str] = []

    def guardar(texto: str) -> str:
        guardados.append(texto)
        return f"\x00{len(guardados) - 1}\x00"

    linea = PROTEGIDO.sub(lambda m: guardar(m.group(0)), linea)

    def sust_ficha(m):
        i = m.group(0)
        if i == propio or i not in fichas or i in hechos:
            return i
        hechos.add(i)
        return guardar(f"[{i}]({rel(uri, fichas[i]['src_uri'])})")

    linea = ID_FICHA.sub(sust_ficha, linea)
    # Las referencias más específicas primero; «ARF» suelto, al final.
    for rid, r in sorted(refs.items(), key=lambda kv: (kv[0] == "ARF", -len(kv[1]["designacion"]))):
        if rid in hechos:
            continue
        for rx in r["_re"]:
            m = rx.search(linea)
            if m:
                hechos.add(rid)
                destino = f"{rel(uri, r['pagina'])}#{r['ancla']}"
                linea = linea[:m.start()] + guardar(f"[{m.group(0)}]({destino})") + linea[m.end():]
                break
    return re.sub(r"\x00(\d+)\x00", lambda m: guardados[int(m.group(1))], linea)


# ------------------------------------------------------------ recuadro y pie

def enlace_ficha(desde: str, i: str) -> str:
    f = _estado["fichas"].get(i)
    return f"[{i}]({rel(desde, f['src_uri'])})" if f else i


def recuadro(markdown: str, uri: str, info: dict) -> str:
    m = info["meta"]
    filas = [("Procedencia", m.get("procedencia")), ("Estado", m.get("estado")),
             ("Fuente", m.get("fuente") or ", ".join(m.get("fuentes") or [])),
             ("Versión de la fuente", m.get("version_fuente")),
             ("Requisitos", ", ".join(map(str, m.get("requisitos") or []))),
             ("Confianza", m.get("confianza")),
             ("Verificado", _verificado(m) or "sin verificar")]
    rb = m.get("revisar_antes")
    if rb:
        aviso = " (vencida)" if _fecha(rb) and _fecha(rb) < HOY else ""
        filas.append(("Revisar antes de", f"{rb}{aviso}"))
    rel_ids = [str(x) for x in (m.get("relacionadas") or [])]
    if rel_ids:
        filas.append(("Relacionadas", ", ".join(enlace_ficha(uri, i) for i in rel_ids)))
    if m.get("url"):
        filas.append(("Documento", f"[abrir]({m['url']})"))
    lista = "\n".join(f"    - **{k}:** {v}" for k, v in filas if v)
    caja = f'!!! abstract "{m.get("id")} · {m.get("estado", "")}"\n\n{lista}\n'
    h1 = re.search(r"^# .+$", markdown, re.M)
    if not h1:
        return caja + "\n" + markdown
    return markdown[:h1.end()] + "\n\n" + caja + markdown[h1.end():]


def pie(uri: str, info: dict, propio: str) -> str:
    refs = _estado["refs"]
    partes = []
    citadas = sorted(info.get("refs", ()), key=lambda r: (refs[r]["organismo"], refs[r]["designacion"]))
    if citadas:
        partes.append("## Documentos citados\n")
        partes += [f"- [{refs[r]['designacion']}]({rel(uri, refs[r]['pagina'])}#{refs[r]['ancla']})"
                   f" · {refs[r]['organismo']}" for r in citadas]
    quienes = sorted(u for u in _estado["ficha_en"].get(propio, ()) if u != uri)
    if quienes:
        partes.append("\n## La citan\n")
        partes += [f"- [{_titulo(u)}]({rel(uri, u)})" for u in quienes]
    return ("\n\n---\n\n" + "\n".join(partes) + "\n") if partes else ""


def _titulo(uri: str) -> str:
    info = _estado["paginas"].get(uri)
    if not info:
        return uri
    i = info["meta"].get("id")
    return f"{i} · {info['titulo']}" if i and es_ficha(info) else info["titulo"]


def _verificado(meta: dict):
    """Fecha de la última comprobación; los criterios la guardan en `fecha`."""
    return meta.get("verificado") or (meta.get("fecha") if meta.get("procedencia") == "criterio" else None)


def _fecha(valor):
    if isinstance(valor, _dt.date):
        return valor
    try:
        return _dt.date.fromisoformat(str(valor))
    except ValueError:
        return None


# ------------------------------------------------------------------ catálogo

def generar_catalogo() -> dict[str, str]:
    refs, citas = _estado["refs"], _estado["citas"]
    citado_por = defaultdict(list)   # ref → actos que la citan
    cita_a = defaultdict(list)       # acto → refs que cita
    for c in citas:
        citado_por[c["ref"]].append(f"acto:{c['acto']}")
        cita_a[f"acto:{c['acto']}"].append(c["ref"])

    por_pagina = defaultdict(list)
    for r in refs.values():
        por_pagina[r["pagina"]].append(r)

    def enlace(desde, rid):
        r = refs.get(rid)
        if not r:
            return rid
        return f"[{r['designacion']}]({rel(desde, r['pagina'])}#{r['ancla']})"

    def bloque(uri, r):
        out = [f"### {r['designacion']} {{ #{r['ancla']} }}\n"]
        if r.get("titulo") and r["titulo"].replace("ETSI ", "") != r["designacion"]:
            out.append(f"{r['titulo']}\n")
        datos = []
        if r.get("version"):
            datos.append(f"- **{'CELEX' if r.get('acto') else 'Versión'}:** {r['version']}")
        if r.get("fecha"):
            datos.append(f"- **Fecha:** {r['fecha']}")
        if r.get("url"):
            tipo = "catálogo de ISO (de pago)" if "iso.org/search" in r["url"] else "abrir el documento"
            datos.append(f"- **Documento:** [{tipo}]({r['url']})")
        else:
            datos.append("- **Documento:** sin enlace público")
        if r.get("acto") and cita_a.get(r["id"]):
            normas = sorted(cita_a[r["id"]], key=lambda x: (refs.get(x, {}).get("organismo", ""), x))
            datos.append("- **Normas que cita:** " + ", ".join(enlace(uri, x) for x in normas))
        if citado_por.get(r["id"]):
            datos.append("- **Citada por:** " + ", ".join(enlace(uri, x) for x in sorted(citado_por[r["id"]])))
        en = sorted(_estado["ref_en"].get(r["id"], ()))
        if en:
            datos.append("- **En el corpus:** " + ", ".join(f"[{_titulo(u)}]({rel(uri, u)})" for u in en))
        if r.get("nota"):
            datos.append(f"- **Nota:** {r['nota']}")
        return "\n".join(out + datos) + "\n"

    paginas = {}
    for uri, lista in por_pagina.items():
        titulo = next(t for p, t, _ in PAGINAS.values() if f"referencias/{p}.md" == uri)
        cuerpo = [f"# {titulo}\n", aviso_generado()]
        if uri == "referencias/legislacion.md":
            for clave, nombre in GRUPOS_ACTOS:
                grupo = [r for r in lista if r.get("grupo") == clave]
                if grupo:
                    cuerpo.append(f"## {nombre}\n")
                    cuerpo += [bloque(uri, r) for r in sorted(grupo, key=_orden_acto)]
            otros = [r for r in lista if not r.get("acto")]
            if otros:
                cuerpo.append("## Otros actos y orientaciones\n")
                cuerpo += [bloque(uri, r) for r in sorted(otros, key=lambda r: r["designacion"])]
        else:
            cuerpo += [bloque(uri, r) for r in sorted(lista, key=lambda r: _orden_natural(r["designacion"]))]
        paginas[uri] = "\n".join(cuerpo)

    filas = []
    for p, t, orden in sorted({v for v in PAGINAS.values()}, key=lambda v: v[2]):
        uri = f"referencias/{p}.md"
        lista = por_pagina.get(uri, [])
        if not lista:
            continue
        con_enlace = sum(1 for r in lista if r.get("url") and "iso.org/search" not in r["url"])
        en_corpus = sum(1 for r in lista if _estado["ref_en"].get(r["id"]))
        filas.append(f"| [{t}]({p}.md) | {len(lista)} | {con_enlace} | {en_corpus} |")
    inv = _estado["inventario"]
    paginas["referencias/index.md"] = "\n".join([
        "# Documentos referenciados\n", aviso_generado(),
        "Catálogo de los documentos que citan los actos de la cartera y de servicios de confianza, "
        "y de los que cita este corpus. Cada entrada enlaza al documento cuando hay una copia pública, "
        "dice qué actos la citan y en qué fichas aparece.\n",
        "| Organismo | Documentos | Con enlace directo | Citados en el corpus |",
        "|---|---|---|---|", *filas, "",
        f"Las citas entre actos y normas salen del [inventario de referencias de Giuseppe De Marco]"
        f"({inv['fuente']}) (Apache-2.0), commit `{inv['commit'][:7]}`, grafo del {inv['grafo_generado']}. "
        "La extracción es automática: una norma que llega por el ARF y no por el texto del acto no "
        "aparece como citada. El resto de entradas se mantiene a mano en `data/referencias.yml`.\n",
    ])
    return paginas


def _orden_natural(texto):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", texto)]


def _orden_acto(r):
    m = re.search(r"(\d{4})/(\d+)", r["designacion"])
    return (0, 0) if not m else (int(m.group(1)), int(m.group(2)))


def aviso_generado() -> str:
    return ("!!! note \"Página generada\"\n    Se construye en cada publicación a partir de "
            "`data/` y de las fichas. No se edita a mano.\n")


# --------------------------------------------------------------------- panel

def generar_panel() -> str:
    fichas = list(_estado["fichas"].values())
    paginas = _estado["paginas"]
    refs = _estado["refs"]

    n_crit = sum(1 for f in fichas if f["src_uri"].startswith("criterios/"))
    por_estado = defaultdict(int)
    por_proc = defaultdict(int)
    for f in fichas:
        por_estado[str(f["meta"].get("estado", "—"))] += 1
        por_proc[str(f["meta"].get("procedencia", "—")).split()[0]] += 1

    previstas = defaultdict(int)
    for uri, info in paginas.items():
        if uri.endswith("README.md"):
            sec = uri.split("/")[0]
            previstas[sec] += len(re.findall(r"^\|[^\n]*\|\s*pendiente[^|\n]*\|\s*$", info["cuerpo"], re.M))

    secciones = []
    for sec, nombre in SECCIONES:
        propias = [f for f in fichas if f["src_uri"].startswith(f"{sec}/")]
        if not propias and not previstas.get(sec):
            continue
        b = sum(1 for f in propias if f["meta"].get("estado") == "borrador")
        rv = sum(1 for f in propias if f["meta"].get("estado") in ("revisado", "vigente"))
        indice = f"{sec}/README.md" if f"{sec}/README.md" in paginas else propias[0]["src_uri"]
        secciones.append(f"| [{nombre}]({indice}) | {len(propias)} | {b} | {rv} | {previstas.get(sec, 0)} |")

    revisar = []
    for f in sorted(fichas, key=lambda f: str(f["meta"].get("revisar_antes") or "9999")):
        rb, ver = _fecha(f["meta"].get("revisar_antes")), _verificado(f["meta"])
        motivo = None
        if not ver:
            motivo = "sin verificar"
        elif rb and rb < HOY:
            motivo = f"revisión vencida ({rb})"
        elif rb and rb - HOY <= VENTANA_REVISION:
            motivo = f"revisar antes de {rb}"
        if motivo:
            revisar.append(f"| [{f['meta']['id']}]({f['src_uri']}) | {f['titulo']} | {motivo} |")

    recientes = sorted((f for f in fichas if _verificado(f["meta"])),
                       key=lambda f: str(_verificado(f["meta"])), reverse=True)[:8]

    actos = (paginas.get("legal/actos.md") or {}).get("cuerpo", "")
    filas_actos = re.findall(r"^\| LEG-\d{3} \|.*\|\s*([^|]*?)\s*\|\s*$", actos, re.M)
    verificados = sum(1 for v in filas_actos if v and v != "—")

    total_refs = len(refs)
    en_corpus = sum(1 for r in refs if _estado["ref_en"].get(r))
    con_enlace = sum(1 for r in refs.values() if r.get("url") and "iso.org/search" not in r["url"])

    def tarjeta(icono, titulo, cifra, texto, enlace):
        return (f"-   :{icono}:{{ .lg .middle }} __{titulo}__\n\n    ---\n\n    **{cifra}** · {texto}\n\n"
                f"    [{enlace[0]}]({enlace[1]})\n")

    tarjetas = "\n".join([
        tarjeta("material-file-document-multiple-outline", "Fichas", len(fichas) - n_crit,
                f"{por_estado.get('borrador', 0)} en borrador, {sum(previstas.values())} previstas",
                ("Por sección", "#fichas-por-seccion")),
        tarjeta("material-scale-balance", "Criterios", n_crit,
                "interpretaciones propias ante ambigüedades", ("Ver criterios", "criterios/README.md")),
        tarjeta("material-bookshelf", "Documentos referenciados", total_refs,
                f"{con_enlace} con enlace directo, {en_corpus} citados en el corpus",
                ("Ir al catálogo", "referencias/index.md")),
        tarjeta("material-gavel", "Tracker legal", len(filas_actos),
                f"filas, {verificados} verificadas en EUR-Lex", ("Ver el tracker", "legal/actos.md")),
    ])

    proc = " · ".join(f"{k}: {v}" for k, v in sorted(por_proc.items()))
    lineas = [
        "---\nhide:\n  - navigation\n---\n",
        "# eudi-corpus\n",
        "Corpus de conocimiento sobre eIDAS 2, la cartera EUDI, el ARF, las normas ETSI e ISO, "
        "OpenID4VC y el perfil europeo de verificación de edad. Cada ficha dice de dónde sale lo que "
        "afirma: **norma**, **observación** o **criterio**. Ver el [método](metodo.md).\n",
        f"!!! info \"Estado a {HOY.isoformat()}\"\n    Este panel se calcula en cada publicación.\n",
        '<div class="grid cards" markdown>\n', tarjetas, "</div>\n",
        "## Fichas por sección\n",
        "| Sección | Escritas | Borrador | Revisadas o vigentes | Previstas |",
        "|---|---|---|---|---|", *secciones, "",
        f"Procedencia de las fichas escritas: {proc}.\n",
        "## Pendiente de revisión\n",
        "Fichas sin verificar, con la revisión vencida o que vencen en los próximos 90 días.\n",
        *(["| Ficha | Título | Motivo |", "|---|---|---|", *revisar] if revisar else ["Nada pendiente."]), "",
        "## Últimas verificaciones\n",
        "| Ficha | Título | Verificada |", "|---|---|---|",
        *[f"| [{f['meta']['id']}]({f['src_uri']}) | {f['titulo']} | {_verificado(f['meta'])} |" for f in recientes],
        "",
    ]
    return "\n".join(lineas)
