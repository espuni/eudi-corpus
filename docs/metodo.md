# Método y reglas del corpus

## Reglas de contenido (no negociables)

1. **Solo fuentes públicas.** Todo lo que entra se apoya en un texto publicado
   o en una observación propia reproducible. Nada que proceda de material
   interno de una empresa, un cliente o un proyecto: ni documentos, ni código,
   ni análisis, ni estructuras copiadas de corpus ajenos.
2. **Sin producto.** El corpus no menciona productos, despliegues, tenants,
   incidencias ni configuraciones de nadie. Si un hallazgo nació trabajando en
   algo concreto, se reescribe en términos genéricos y reproducibles.
3. **Sin personas.** No hay contactos ni nombres de personas. Como mucho, el
   canal público (foro, repositorio, lista de correo) donde se discute un tema.
4. **Respetar las licencias de las fuentes:**
   - EUR-Lex: reutilizable citando la fuente. Se pueden citar artículos.
   - ETSI: descarga gratuita, pero con copyright. Se cita la cláusula y el ID
     del requisito y se resume con palabras propias; no se copian párrafos.
   - ISO/IEC: de pago. **Nunca** se reproduce texto ni tablas; solo referencias
     a cláusulas.
   - OpenID, IETF, W3C, ARF: comprobar la licencia de cada documento antes de
     citar literalmente; por defecto, resumir.
5. **Citar al requisito, no al documento.** «TS 119 602, GEN-5.2.4-04» vale;
   «según la TS 119 602» no.
6. **Fijar la versión.** Cada ficha declara la versión exacta de la fuente
   (`ARF 1.x.y`, `draft-ietf-oauth-status-list-NN`, `OpenID4VP 1.0`). Nunca
   enlaces a `latest`.

## Procedencia

| Valor | Significa | Ejemplo |
|---|---|---|
| `norma` | Lo dice el texto citado | «La WIA va al PAR y al token» |
| `observacion` | Medido en la práctica; ninguna norma lo dice | «El túnel cross-device no devuelve una prueba de 360 KB» |
| `criterio` | Interpretación propia ante una ambigüedad | «Tratamos X como obligatorio aunque la TS dice *should*» |

Una ficha puede mezclar procedencias por apartados; en ese caso se marca cada
apartado.

## Ciclo de vida de una ficha

`borrador` → `revisado` → (`obsoleto` cuando cambia la fuente).

Cuando sale una versión nueva de una fuente: se actualiza `legal/actos.md` o
`fuentes.md`, se buscan las fichas con la versión antigua y se revisan.
Lo perecedero (estado de borradores, fechas de aplicación aún no cumplidas)
lleva `revisar_antes`.

## Convenciones

- Una ficha, un tema. Nombre de fichero en minúsculas con guiones.
- `id` estable con prefijo de carpeta (`LEG-`, `ARF-`, `PRO-`, `FMT-`, `CNF-`,
  `AV-`, `OBS-`, `CRI-`, `EVA-`). No se reutiliza nunca.
- Idioma: español; los nombres normativos van como se publican
  (Trusted List, Access Certificate, DCQL…).
