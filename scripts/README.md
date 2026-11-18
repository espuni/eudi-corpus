# Scripts

## `importar_inventario.py`

Genera `data/inventario.json` (actos, normas que citan y citas acto → norma) a partir del
inventario [eidas-references-search-engine](https://github.com/peppelinux/eidas-references-search-engine)
(Giuseppe De Marco, Apache-2.0). Lee solo su `manifest.yaml` y
`report/references-graph.json`.

```bash
git clone https://github.com/peppelinux/eidas-references-search-engine.git /tmp/inventario
git -C /tmp/inventario checkout <commit>
python3 -I scripts/importar_inventario.py /tmp/inventario "$(git -C /tmp/inventario rev-parse HEAD)"
```

Requiere PyYAML. Commit importado la última vez: `300f644` (grafo del 2026-07-29).
Corrige dos ids mal extraídos por el inventario (ver `CORRECCIONES`). Al
reimportar, revisar el diff: un acto nuevo o una cita nueva suele implicar
actualizar `docs/legal/actos.md` y alguna ficha.

El sitio (`hooks/corpus.py`) combina ese fichero con `data/referencias.yml`,
que se mantiene a mano, para generar el panel y el catálogo de documentos.

## `vigilar_fuentes.py`

Revisión periódica de las fuentes de [`data/fuentes.yml`](../data/fuentes.yml).
Para las que viven en GitHub (ARF, especificaciones de la Comisión, verificación
de edad, OpenID, borradores IETF, DC API, longfellow, inventario de De Marco)
mira si hay etiquetas de versión posteriores a la citada y commits posteriores a
la última revisión; para todas, si su revisión manual ha vencido. Escribe un
informe en Markdown y no modifica nada.

```bash
python3 -I scripts/vigilar_fuentes.py                 # informe por pantalla
python3 -I scripts/vigilar_fuentes.py --sin-red       # solo vencimientos
python3 -I scripts/vigilar_fuentes.py --solo arf av-spec
```

Lo ejecuta cada mes el flujo `vigilar-fuentes`, que abre un issue
`revision-fuentes` (o comenta en el que siga abierto). Requiere `git` y PyYAML.
EUR-Lex, ETSI, ISO y las erratas de RFC no tienen un sitio que se pueda consultar
solo con fiabilidad: se revisan a mano con la periodicidad de cada entrada.
