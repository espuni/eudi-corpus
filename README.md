# eudi-corpus

Corpus de conocimiento sobre el marco europeo de identidad digital (eIDAS 2,
EUDI Wallet, ARF, normas ETSI/ISO, OpenID4VC y el perfil europeo de
verificación de edad). Está pensado para dos usos:

- **consulta humana**: fichas cortas, con la fuente primaria y la versión exacta;
- **contexto para asistentes de IA**: cada ficha declara de dónde sale lo que
  dice, para que una IA no presente una opinión como si fuera norma.

## Qué es y qué no es

- **Es** un mapa de las normas y de cómo encajan, con citas al requisito
  concreto (artículo, cláusula, ID de requisito) y criterios de interpretación
  firmados como tales.
- **No es** una copia de las normas. Se enlaza y se resume; no se reproduce
  texto de ETSI ni de ISO (ver [el método](docs/metodo.md)).
- **No es** documentación de ningún producto ni de ningún cliente o empleador.
  No contiene configuraciones, código, incidencias ni contactos de nadie.

## Sitio publicado

**https://espuni.github.io/eudi-corpus/** — se publica en GitHub Pages en cada
push a `main` (`.github/workflows/pages.yml`). Incluye:

- un **panel** con el estado de las fichas, lo pendiente de revisión y el
  tracker legal;
- un **catálogo de documentos referenciados**, una página por organismo, con el
  enlace a cada documento cuando hay copia pública, qué actos lo citan y en qué
  fichas aparece;
- **enlaces automáticos** en las fichas a los documentos del catálogo y a otras
  fichas.

Para verlo en local:

```bash
pip install -r requirements.txt
mkdocs serve
```

`mkdocs build --strict` falla si hay enlaces rotos; es lo que comprueba la CI.

## Estructura

| Ruta | Contenido |
|---|---|
| [`docs/legal/`](docs/legal/) | Tracker de reglamentos y actos de ejecución |
| [`docs/arf/`](docs/arf/) | ARF (versión fijada) y especificaciones técnicas de la Comisión |
| [`docs/protocolos/`](docs/protocolos/) | OpenID4VCI, OpenID4VP, HAIP, DCQL, Digital Credentials API, Token Status List |
| [`docs/formatos/`](docs/formatos/) | ISO/IEC 18013-5 y TS 18013-7 (mdoc), SD-JWT VC |
| [`docs/confianza/`](docs/confianza/) | Trusted Lists, LoTE, certificados de acceso y de registro, perfiles X.509 |
| [`docs/edad/`](docs/edad/) | EU Age Verification Blueprint y su perfil |
| [`docs/observaciones/`](docs/observaciones/) | Comportamientos medidos que no están en ninguna norma |
| [`docs/criterios/`](docs/criterios/) | Criterios de interpretación ante ambigüedades |
| [`docs/evaluacion/`](docs/evaluacion/) | Preguntas para evaluar a un asistente de IA |
| [`docs/plantillas/`](docs/plantillas/) | Plantillas de ficha, criterio y pregunta |
| [`data/`](data/) | `inventario.json` (generado) y `referencias.yml` (a mano): el catálogo |
| [`hooks/corpus.py`](hooks/corpus.py) | Genera el panel, el catálogo y los enlaces en cada build |
| [`scripts/`](scripts/) | Importación del inventario de referencias |

Además: [`docs/metodo.md`](docs/metodo.md) (reglas del corpus),
[`docs/fuentes.md`](docs/fuentes.md) y [`docs/glosario.md`](docs/glosario.md).

## Cómo leer una ficha

Cada ficha empieza con un bloque de metadatos (en el sitio se muestra como un recuadro). Los dos campos que más importan:

- `procedencia`: `norma` (lo dice el texto citado), `observacion` (se ha medido,
  no lo dice ninguna norma) o `criterio` (interpretación propia ante una
  ambigüedad). Una IA que use el corpus debe distinguir los tres.
- `version_fuente` y `verificado`: contra qué versión exacta se escribió y cuándo
  se comprobó por última vez. Una ficha sin versión no es fiable.

## Licencia

Textos propios bajo [CC BY 4.0](LICENSE). Las normas citadas pertenecen a sus
autores y se rigen por sus propias licencias. El catálogo de actos y citas deriva de
[eidas-references-search-engine](https://github.com/peppelinux/eidas-references-search-engine),
de Giuseppe De Marco, bajo licencia Apache-2.0.
