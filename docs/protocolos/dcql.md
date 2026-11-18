---
id: PRO-004
titulo: "DCQL: cómo se pide una credencial en OpenID4VP"
procedencia: mixta          # norma (§1-§4) · criterio (§5)
fuente: "OpenID for Verifiable Presentations 1.0, final (2025-07-09), §6, §7 y apéndice B"
version_fuente: "OpenID4VP 1.0 final, 2025-07-09"
url: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html
requisitos: ["OpenID4VP §6.1, §6.1.1, §6.2, §6.3, §6.4", "§7", "B.2.3", "B.2.4"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [dcql, openid4vp, trusted-authorities, mdoc, sd-jwt-vc, minimizacion]
relacionadas: [PRO-002, PRO-010, CRI-003, CNF-007]
---

# DCQL

## En una frase

DCQL es un JSON con una lista de **consultas de credencial** (formato,
metadatos, atributos y, opcionalmente, autoridades de confianza) y, si hace
falta, **conjuntos** que dicen qué combinaciones valen.

## 1. Estructura

```json
{
  "credentials": [{
    "id": "edad",
    "format": "mso_mdoc",
    "meta": { "doctype_value": "eu.europa.ec.av.1" },
    "claims": [{ "path": ["eu.europa.ec.av.1", "age_over_18"], "values": [true] }],
    "trusted_authorities": [{ "type": "etsi_tl", "values": ["https://…/av-tl.xml"] }]
  }]
}
```

| Campo | Obligatorio | Qué hace |
|---|---|---|
| `credentials` | Sí | Lista de consultas de credencial (§6) |
| `credential_sets` | No | Combinaciones válidas de consultas: `options` y `required` (§6.2) |
| `id` | Sí | Identifica la consulta en la respuesta |
| `format` | Sí | `mso_mdoc`, `dc+sd-jwt`… (apéndice B) |
| `meta` | **Sí**, aunque sea vacío | Restricciones por formato. En mdoc, `doctype_value` (B.2.3) |
| `claims` | No | Atributos pedidos, cada uno con `path` y, opcionalmente, `values` (§6.3) |
| `claim_sets` | No | Combinaciones de atributos (§6.1, §6.4.1) |
| `multiple` | No | Si se admiten varias credenciales (por defecto, no) |
| `require_cryptographic_holder_binding` | No | Por defecto `true` |
| `trusted_authorities` | No | Emisores que el verificador aceptará (§6.1.1) |

En mdoc, cada atributo puede llevar `intent_to_retain` (B.2.4). El `path` de un
mdoc es `[namespace, elemento]` (§7.2).

## 2. Reglas de selección (§6.4)

- **Sin `claims`**: solo se devuelve lo que no es divulgable de forma
  selectiva.
- **Con `claims` y sin `claim_sets`**: se piden todos los atributos listados.
- La cartera **no envía** atributos divulgables de forma selectiva que no se
  hayan pedido.
- Con `values`, la cartera **debería** devolver el atributo solo si coincide
  tipo y valor. En mdoc, el valor CBOR se convierte a JSON antes de comparar.

## 3. Autoridades de confianza (§6.1.1)

| Tipo | Valor | Coincide si |
|---|---|---|
| `aki` | Identificador de clave de la autoridad, en base64url | Algún certificado de la cadena de la credencial tiene ese AKI |
| `etsi_tl` | Identificador de una Trusted List (TS 119 612) | Algún certificado de la cadena está en la lista o en sus listas en cascada |
| `openid_federation` | Identificador de entidad | Se puede construir una ruta de confianza válida |

**Importante**: el verificador **tiene que validar por su cuenta** que el
emisor es de confianza. `trusted_authorities` sirve sobre todo para
**minimizar datos**, para no revelar algo que se rechazaría (§6.1).

## 4. Extensibilidad

Las implementaciones **ignoran** las propiedades que no conocen (§6).

## 5. Lo que conviene tener claro (procedencia: criterio)

- **«Ignorar lo desconocido» no es lo que se observa.** La especificación
  manda ignorar propiedades desconocidas, pero hay carteras que rechazan la
  petición entera por un campo de más en `meta` (ver
  [PRO-010](perfiles-oid4vp-identificacion-del-verifier.md)). Emitir solo lo
  necesario sigue siendo lo más interoperable.
- **`values` no es un control.** Es un *should* para la cartera. Si el
  verificador necesita `age_over_18 = true`, lo comprueba en la respuesta, no
  se fía de que la cartera haya filtrado.
- **Sin lista de confianza, no hay validación del emisor**: ver
  [CRI-003](../criterios/sin-lista-no-se-valida.md). La propia especificación
  lo confirma: `trusted_authorities` no sustituye a la validación.
