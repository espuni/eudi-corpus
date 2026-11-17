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
  texto de ETSI ni de ISO (ver [METODO.md](METODO.md)).
- **No es** documentación de ningún producto ni de ningún cliente o empleador.
  No contiene configuraciones, código, incidencias ni contactos de nadie.

## Estructura

| Carpeta | Contenido |
|---|---|
| [`legal/`](legal/) | Reglamentos y actos de ejecución. [`actos.md`](legal/actos.md) es el tracker |
| [`arf/`](arf/) | Architecture and Reference Framework, con versión fijada |
| [`protocolos/`](protocolos/) | OpenID4VCI, OpenID4VP, HAIP, DCQL, Digital Credentials API, Token Status List |
| [`formatos/`](formatos/) | ISO/IEC 18013-5 y TS 18013-7 (mdoc), SD-JWT VC |
| [`confianza/`](confianza/) | Trusted Lists, LoTE, certificados de acceso y de registro, perfiles X.509 |
| [`edad/`](edad/) | EU Age Verification Blueprint y su perfil (Anexo A) |
| [`observaciones/`](observaciones/) | Comportamientos medidos en la práctica que no están en ninguna norma |
| [`criterios/`](criterios/) | Registro de criterios de interpretación ante ambigüedades |
| [`evaluacion/`](evaluacion/) | Preguntas con respuesta de referencia para evaluar a un asistente de IA |
| [`plantillas/`](plantillas/) | Plantillas de ficha, criterio y pregunta |

Además: [`fuentes.md`](fuentes.md) (URL canónicas de cada fuente),
[`glosario.md`](glosario.md) y [`scripts/`](scripts/), que genera las tablas
derivadas del inventario de referencias de Giuseppe De Marco
(`legal/actos-inventario.md`, `legal/matriz-actos-normas.md`).

## Cómo leer una ficha

Cada ficha empieza con un bloque de metadatos. Los dos campos que más importan:

- `procedencia`: `norma` (lo dice el texto citado), `observacion` (se ha medido,
  no lo dice ninguna norma) o `criterio` (interpretación propia ante una
  ambigüedad). Una IA que use el corpus debe distinguir los tres.
- `version_fuente` y `verificado`: contra qué versión exacta se escribió y cuándo
  se comprobó por última vez. Una ficha sin versión no es fiable.

## Licencia

Textos propios bajo [CC BY 4.0](LICENSE). Las normas citadas pertenecen a sus
autores y se rigen por sus propias licencias. Las tablas de `legal/` marcadas
como generadas derivan de
[eidas-references-search-engine](https://github.com/peppelinux/eidas-references-search-engine),
de Giuseppe De Marco, bajo licencia Apache-2.0.
