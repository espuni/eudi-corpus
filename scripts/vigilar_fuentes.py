"""Revisión periódica de las fuentes del corpus.

Para cada fuente de `data/fuentes.yml`:

- si se vigila con `git`, mira en GitHub si hay etiquetas de versión
  posteriores a la citada y cuántos commits hay desde la versión citada (o
  desde la última revisión) en las rutas que interesan;
- en todos los casos, calcula si su revisión manual ha vencido.

Escribe un informe en Markdown, pensado para un issue. No modifica nada: quien
revisa actualiza `data/fuentes.yml` a mano.

    python3 -I scripts/vigilar_fuentes.py --salida informe.md
    python3 -I scripts/vigilar_fuentes.py --sin-red        # solo vencimientos

Sale con código 0 aunque haya cambios; `--resumen` escribe en un fichero
aparte `cambios=N` y `pendientes=N` para el flujo de GitHub Actions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import pathlib
import re
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "hooks"))
import fuentes as F  # noqa: E402

MAX_COMMITS = 8


def git(*args, cwd=None) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} falló")
    return r.stdout


def orden_natural(texto: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", texto)]


def etiquetas_nuevas(repo: str, patron: str, citada: str | None) -> tuple[list[str], str | None]:
    """Etiquetas que casan con el patrón y van después de la citada."""
    salida = git("ls-remote", "--tags", f"https://github.com/{repo}.git")
    tags = sorted({ln.split("refs/tags/")[1].removesuffix("^{}")
                   for ln in salida.splitlines() if "refs/tags/" in ln}, key=orden_natural)
    tags = [t for t in tags if fnmatch.fnmatch(t, patron)]
    actual = None
    if citada:
        en_citada = [t for t in tags if re.search(rf"(?<![\w.-]){re.escape(t)}(?![\w.]|-\d)", citada)]
        actual = max(en_citada, key=orden_natural) if en_citada else None
    if actual is None:
        return tags[-1:], None
    return [t for t in tags if orden_natural(t) > orden_natural(actual)], actual


def commits_desde(repo: str, base: str | None, desde: dt.date | None, rutas: list[str]) -> tuple[list[str], str]:
    """Commits de la rama principal posteriores a `base` y a la fecha `desde`
    (la última revisión). Sin fecha, todos los posteriores a `base`."""
    with tempfile.TemporaryDirectory() as tmp:
        git("clone", "--quiet", "--bare", "--filter=blob:none",
            f"https://github.com/{repo}.git", tmp)
        rango, criterio = ["HEAD"], "en la rama principal"
        if base:
            try:
                git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}", cwd=tmp)
                rango, criterio = [f"{base}..HEAD"], f"desde `{base[:7] if len(base) == 40 else base}`"
            except RuntimeError:
                criterio = f"(no se encuentra `{base}`; se cuenta desde la última revisión)"
        if rango == ["HEAD"] and not desde:
            return [], "sin versión ni fecha de referencia"
        if desde:
            # Lo anterior a la última revisión ya se vio: solo cuenta lo nuevo.
            rango.append(f"--since={desde.isoformat()}T23:59:59Z")
            criterio += f" y posteriores a la revisión del {desde.isoformat()}"
            if rango[0] == "HEAD":
                criterio = f"posteriores a la revisión del {desde.isoformat()}"
        log = git("log", "--format=%h %as %s", *rango, "--", *rutas, cwd=tmp)
        return [ln for ln in log.splitlines() if ln.strip()], criterio


def revisar(f: dict, hoy: dt.date, con_red: bool) -> dict:
    clave, proxima = F.estado(f, hoy)
    res = {"f": f, "estado": clave, "proxima": proxima, "cambios": [], "error": None}
    v = f["vigilar"]
    if not con_red or v["metodo"] != "git":
        return res
    try:
        base = v.get("base")
        if v.get("etiquetas"):
            # `vista`: la última etiqueta ya revisada aunque se siga citando otra
            # (un acto puede fijar un borrador anterior a propósito).
            nuevas, actual = etiquetas_nuevas(v["repo"], v["etiquetas"],
                                              v.get("vista") or base or f.get("citada"))
            if nuevas and (actual or not f.get("citada")):
                res["cambios"].append(
                    f"Etiquetas posteriores a `{actual}`: " + ", ".join(f"`{t}`" for t in nuevas[-5:])
                    if actual else f"Última etiqueta: `{nuevas[-1]}` (la versión citada está por fijar)")
        commits, criterio = commits_desde(v["repo"], base, f.get("revisado"), v.get("rutas") or [])
        if commits:
            donde = f" en `{', '.join(v['rutas'])}`" if v.get("rutas") else ""
            lista = "".join(f"\n    - `{c}`" for c in commits[:MAX_COMMITS])
            mas = f"\n    - … y {len(commits) - MAX_COMMITS} más" if len(commits) > MAX_COMMITS else ""
            res["cambios"].append(f"{len(commits)} commits {criterio}{donde}:{lista}{mas}")
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        res["error"] = str(e).splitlines()[0][:200]
    return res


def informe(resultados: list[dict], hoy: dt.date, url_sitio: str) -> str:
    def titulo(f):
        return f"[{f['nombre']}]({url_sitio}fuentes/#{f['id']})"

    def mirar(f):
        texto, url = F.url_vigilar(f)
        return f"[{texto}]({url})"

    con_cambios = [r for r in resultados if r["cambios"]]
    errores = [r for r in resultados if r["error"]]
    vencidas = [r for r in resultados if r["estado"] in ("vencida", "pronto") and not r["cambios"]]
    nunca = [r for r in resultados if r["estado"] == "sin-revisar" and not r["cambios"]]
    al_dia = len(resultados) - len(con_cambios) - len(vencidas) - len(nunca)

    out = [f"## Revisión de fuentes del {hoy.isoformat()}\n",
           f"{len(con_cambios)} con cambios detectados · {len(vencidas)} con la revisión vencida o a "
           f"punto de vencer · {len(nunca)} sin revisar nunca · {al_dia} al día.\n",
           "Tras revisar cada una: fecha de hoy en `revisado` de `data/fuentes.yml` y, si cambió "
           "de versión, `citada`, `url` y `base`, más las fichas y fuentes que lista su entrada del "
           f"[seguimiento]({url_sitio}fuentes/).\n"]
    if con_cambios:
        out.append("### Cambios detectados en GitHub\n")
        for r in con_cambios:
            out.append(f"- [ ] {titulo(r['f'])} (citada: {r['f'].get('citada') or 'por fijar'})")
            out += [f"  - {c}" for c in r["cambios"]]
        out.append("")
    if vencidas:
        out.append("### Revisión manual que toca\n")
        for r in sorted(vencidas, key=lambda r: r["proxima"]):
            out.append(f"- [ ] {titulo(r['f'])}: tocaba el {r['proxima'].isoformat()} · {mirar(r['f'])}")
        out.append("")
    if nunca:
        out.append("### Sin revisar nunca contra el texto\n")
        for r in nunca:
            out.append(f"- [ ] {titulo(r['f'])} · {mirar(r['f'])}")
        out.append("")
    if errores:
        out.append("### No se pudieron comprobar\n")
        out += [f"- {titulo(r['f'])}: {r['error']}" for r in errores]
        out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--salida", type=pathlib.Path, help="fichero del informe (por defecto, stdout)")
    p.add_argument("--resumen", type=pathlib.Path, help="fichero con cambios=N y pendientes=N")
    p.add_argument("--hoy", type=dt.date.fromisoformat, default=dt.date.today())
    p.add_argument("--sin-red", action="store_true", help="no consultar GitHub")
    p.add_argument("--solo", nargs="*", help="ids de fuente que revisar")
    p.add_argument("--sitio", default="https://espuni.github.io/eudi-corpus/")
    a = p.parse_args(argv)

    fuentes = F.cargar(RAIZ)
    if a.solo:
        fuentes = [f for f in fuentes if f["id"] in a.solo]
    resultados = [revisar(f, a.hoy, not a.sin_red) for f in fuentes]
    texto = informe(resultados, a.hoy, a.sitio)
    if a.salida:
        a.salida.write_text(texto, encoding="utf-8")
    else:
        print(texto)
    if a.resumen:
        cambios = sum(1 for r in resultados if r["cambios"])
        pendientes = sum(1 for r in resultados if r["cambios"] or r["estado"] != "al-dia")
        a.resumen.write_text(f"cambios={cambios}\npendientes={pendientes}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
