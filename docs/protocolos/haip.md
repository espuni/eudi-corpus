---
id: PRO-003
titulo: "HAIP 1.0: qué exige y qué cambia el perfil EUDI"
procedencia: mixta          # norma (§1-§4) · criterio (§5)
fuente: "OpenID4VC High Assurance Interoperability Profile 1.0, final (24-12-2025); ETSI TS 119 472-2 V1.2.1 y TS 119 472-3 V1.1.1 con las adaptaciones de 2026/1731"
version_fuente: "HAIP 1.0 final, 2025-12-24"
url: https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html
requisitos: ["HAIP 4, 4.1-4.5.1", "HAIP 5, 5.1, 5.2, 5.3", "HAIP 6.1", "HAIP 7", "HAIP 8"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [haip, openid4vci, openid4vp, dpop, pkce, x509-hash, cifrado, dc-api]
relacionadas: [CNF-007, CNF-008, PRO-010, PRO-002, PRO-001]
---

# HAIP 1.0 y el perfil EUDI

## En una frase

HAIP perfila OpenID4VCI y OpenID4VP para alta garantía. El perfil EUDI
(TS 119 472-2 y -3) se apoya en él, lo endurece en algunos puntos y en otros lo
relaja, y **lo que dice la TS prevalece** sobre HAIP (OIDFVP-HAIP-GEN-03).

## 1. Emisión (HAIP 4)

| HAIP exige | En el perfil EUDI |
|---|---|
| Flujo *authorization code* para cartera **y** emisor | La cartera, los dos flujos; el emisor, **al menos uno** (TS 119 472-3 GEN-REQ-4.1-03 y -04) |
| PKCE con S256, PAR (si se usa el *authorization endpoint*) e `iss` en la respuesta, según FAPI 2.0 | Se mantiene |
| **DPoP** para atar el token de acceso | Se mantiene |
| `scope` en los metadatos para cada configuración de credencial, y en la petición | Se mantiene |
| *Nonce endpoint* obligatorio si alguna credencial va ligada a una clave | Se mantiene |
| Metadatos firmados **si el ecosistema lo pide**, con `x5c` sin el ancla y certificado no autofirmado | El perfil EUDI **los exige**, firmados con el certificado de acceso (ISS-MDATA-4.2.1-01 y -02) |
| Autenticación de la cartera con atestación en PAR y token. La atestación **no se reutiliza entre emisores** y no lleva un identificador único de la instancia | WIA según el anexo III de 2026/1731 (TR-WIA-3.2) |
| Atestación de claves con pruebas `jwt` y `attestation` (*SHOULD*) | **Obligatorio** admitir las dos en credenciales ligadas al dispositivo (TR_KA-4) |
| *Refresh tokens* recomendados | Opcionales (TOKEN-REQ-PROC-4.5.2-04) |
| Esquema `haip-vci://` opcional | Esquema **`eu-eaa-offer://`** obligatorio (GEN-REQ-4.1-06) |

## 2. Presentación (HAIP 5)

Para cualquier flujo:

- `response_type=vp_token` y consulta **DCQL** (OpenID4VP §6).
- Peticiones firmadas con el prefijo **`x509_hash`**. El certificado del ancla
  no va en `x5c` y el que firma no puede ser autofirmado.
- **Respuesta cifrada** (OpenID4VP 8.3) con ECDH-ES sobre P-256. El verificador
  admite A128GCM **y** A256GCM y anuncia los dos; la cartera, al menos uno. Las
  claves de cifrado son **efímeras, una por petición**.
- La consulta de autoridades de confianza por **identificador de clave de la
  autoridad (`aki`)** es obligatoria. El perfil EUDI añade el tipo
  **`etsi_tl`** (TS 119 472-2 RO-17).

**Por redirección (HAIP 5.1):** JAR con `request_uri`; respuesta
`direct_post.jwt`; el flujo en el mismo dispositivo es obligatorio y el
cross-device, desaconsejado. El verificador rechaza la presentación si la
cartera no vuelve por la redirección o vuelve a otra sesión.

**Por la Digital Credentials API (HAIP 5.2):** respuesta `dc_api.jwt`; la
cartera admite peticiones sin firmar, firmadas y multifirma, y el verificador
al menos una de las tres. **El perfil EUDI lo cambia**: la cartera **no** admite
`openid4vp-1-unsigned` (TS 119 472-2 API-03).

## 3. Formatos (HAIP 5.3 y 6)

- mdoc: formato `mso_mdoc`; varios mdoc van en `DeviceResponse` separados; la
  revocación del MSO, si existe, según ISO/IEC 18013-5 2.ª edición.
- SD-JWT VC: formato `dc+sd-jwt`; serialización compacta (RFC 9901);
  certificado del emisor en `x5c` con su cadena; KB-JWT siempre que haya
  vínculo con el titular. La claim `status`, si existe, lleva `status_list`. El
  firmante de la lista de estado va en `x5c`, y cada credencial tiene su propio
  índice impredecible en la lista.

## 4. Algoritmos (HAIP 7 y 8)

ES256 (P-256 y SHA-256) como mínimo en todas las firmas que se validan, y
SHA-256 para los resúmenes de SD-JWT VC y mdoc.

## 5. Lo que conviene tener claro (procedencia: criterio)

- **Las anulaciones de 2026/1731 en TS 119 472-2 no relajan nada.** El acto
  deja sin efecto, en la TS, `x509_hash`, el cifrado de la respuesta y la
  petición por referencia, pero HAIP 5 y 5.1 los siguen exigiendo, y el acto
  aplica HAIP. Lo que quitó fue una duplicación.
- **El perfil EUDI es más estricto que HAIP en dos sitios** que conviene
  probar: rechazo de peticiones sin firmar por la DC API, y admisión de los dos
  tipos de prueba de clave.
