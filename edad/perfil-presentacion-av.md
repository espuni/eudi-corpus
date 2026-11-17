---
id: AV-002
titulo: "Perfil de presentación de AV (anexo A §A.6-§A.10): ZK, DC API y fallback OpenID4VP"
procedencia: mixta          # norma (§1-§4) · observacion (§5)
fuente: "av-doc-technical-specification, anexo A, commit 8b97287 (2026-09-02)"
version_fuente: "commit 8b97287"
url: https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/annexes/annex-A/annex-A-av-profile.md
requisitos: ["Anexo A §A.6", "§A.7", "§A.8", "§A.9", "§A.10", "Spec. principal §4.4"]
estado: borrador
verificado: 2026-11-17
revisar_antes: 2027-03-01
tags: [verificacion-de-edad, presentacion, dc-api, oid4vp, zk, longfellow, mdoc]
relacionadas: [AV-001, AV-003, PRO-010, OBS-001, FMT-002]
---

# Perfil de presentación de AV

## En una frase

La prueba de edad se presenta preferentemente como **prueba de conocimiento cero
sobre la Digital Credentials API**; si el dispositivo no la soporta, como mdoc
simple; y si no hay DC API, por **OpenID4VP sin firmar, por valor y con
`redirect_uri`**.

## 1. Mecanismo y transporte (§A.6)

Son dos elecciones dependientes:

| | DC API (por defecto) | OpenID4VP (fallback de transporte) |
|---|---|---|
| Prueba ZK (preferida) | Sí | **No**: no hay consulta DCQL estandarizada para ZK |
| mdoc simple | Si el dispositivo no genera ZK | Siempre |

- El mdoc simple se usa **solo** si el dispositivo no genera ZK o si el
  transporte es OpenID4VP.
- La RP **no debe rechazar** una presentación solo por venir en mdoc simple:
  no puede distinguir un dispositivo sin ZK de una degradación (§A.9).

## 2. DC API (ISO/IEC TS 18013-7, anexo C)

- Petición: `encryptionInfo` (`["dcapi", {nonce, recipientPublicKey}]`) y
  `deviceRequest` (ISO/IEC 18013-5 §8.3.2.1.2.1), ambos CBOR en base64url sin
  relleno.
- Respuesta: `["dcapi", {enc, cipherText}]`, un `DeviceResponse` cifrado
  con **HPKE** (RFC 9180).
- **Sin autenticación del lector** (*reader authentication* fuera de alcance).

## 3. Fallback OpenID4VP

- Invocación de la app: al menos el esquema **`av://`**.
- `response_type=vp_token`, `response_mode=direct_post` (no `.jwt`).
- Petición como parámetros en la URL: **`request` y `request_uri` NO deben
  usarse** (sin JAR).
- Identificador de cliente: prefijo **`redirect_uri`** seguido del
  `response_uri`.
- `nonce` obligatorio; `state` opcional; DCQL según OpenID4VP §6.
- Sin autenticación de cliente.

**Por qué (§A.10, informativo).** Sin una lista de confianza de RP, firmar la
petición no aporta seguridad: cualquiera puede conseguir un certificado válido y
sustituir un JAR legítimo. El modelo de amenazas confía en TLS/Web PKI y excluye
CA maliciosas, así que tampoco se cifra la respuesta.

## 4. Pruebas de conocimiento cero (§A.8)

- Sistema único: **`longfellow-libzk-v1`** (Frigo y shelat, *Anonymous
  credentials from ECDSA*; borrador IETF `draft-google-cfrg-libzk`).
  Implementar otro sistema no es conformidad con el perfil.
- Estructura de petición y respuesta: `ZkSystemSpec` de ISO/IEC 18013-5,
  2.ª edición, §10.2.7, sobre la DC API del anexo C.
- La prueba demuestra: firma del AP verificable, atributo pedido presente y
  `true`, firma del nonce con la clave del dispositivo y atestación dentro de
  su validez.
- La app *SHALL* generar ZK si la plataforma lo soporta.
- La RP *SHALL* verificar ZK y **comprobar el hash del circuito contra la lista
  de circuitos aceptados** antes de verificar la prueba; un circuito no aceptado
  se rechaza. La lista de circuitos la publica el responsable del esquema, fuera
  del documento.
- La RP *SHALL* aceptar también el fallback mdoc.

## 5. Lo observado en la práctica (procedencia: observacion)

- **Julio de 2026:** la app de referencia aceptaba también peticiones
  OpenID4VP **firmadas y por referencia** (`request_uri`) y el esquema
  `openid4vp://`. Es más de lo que exige el perfil; una app nacional que lo
  implemente al pie de la letra puede no hacerlo. Hay que probar cada app.
- **Agosto de 2026:** la prueba ZK (~360 KB) no vuelve por el flujo
  cross-device de la DC API; ver [OBS-001](../observaciones/zk-cross-device.md).
  Con la ZK ya como mecanismo preferido, el impacto es mayor: en escritorio
  queda el fallback.
