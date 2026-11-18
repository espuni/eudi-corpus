---
id: PRO-010
titulo: "Perfiles de OpenID4VP: identificación del verifier, cifrado de la respuesta y handover"
procedencia: mixta          # norma (§1-§3) · observacion (§4)
fuente: "OpenID4VP 1.0; HAIP 1.0; ISO/IEC TS 18013-7 anexo C; EU AV Blueprint, anexo A"
version_fuente: "OpenID4VP 1.0 final (2025-07-09); HAIP 1.0 final (2025-12-24); AV anexo A commit 8b97287"
url: ""
requisitos: ["AV anexo A §A.6", "AV anexo A §A.8", "ISO/IEC TS 18013-7 anexo C"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [oid4vp, haip, dc-api, mdoc, verificacion-de-edad, dcql]
relacionadas: [PRO-002, PRO-003, PRO-004, FMT-002, AV-002, OBS-001, CRI-003]
---

# Perfiles de OpenID4VP: identificación del verifier, cifrado y handover

## En una frase

«Usar OpenID4VP» no fija cómo se identifica el verifier, si la petición va
firmada ni si la respuesta va cifrada: eso lo decide el perfil, y en el mundo
EUDI conviven al menos tres, que no son intercambiables.

## 1. Los tres perfiles (procedencia: norma)

Verificado contra el anexo A de AV (commit `8b97287`, ver
[AV-002](../edad/perfil-presentacion-av.md)), HAIP 1.0 final §5, 5.1 y 5.2 y
OpenID4VP 1.0 final §5.9.3.

| | Firmado (HAIP) | Fallback de AV | DC API con `org-iso-mdoc` |
|---|---|---|---|
| Dónde se define | HAIP 1.0 sobre OpenID4VP 1.0 | AV anexo A §A.6 | ISO/IEC TS 18013-7 anexo C; AV anexo A §A.8 para ZK |
| Identificación del verifier | `client_id` con prefijo `x509_hash:` (hash del certificado hoja) | `client_id` con prefijo `redirect_uri:` seguido del `response_uri` | No hay `client_id` de OpenID4VP |
| Petición | Firmada (JAR, `typ` `oauth-authz-req+jwt`, cadena en `x5c`) | **Sin firmar, por valor**: `request` y `request_uri` no deben usarse | `DeviceRequest` CBOR |
| Modo de respuesta | `direct_post.jwt` o `dc_api.jwt` | `direct_post` | Respuesta de la DC API |
| Cifrado de la respuesta | JWE con clave efímera del verifier en `client_metadata.jwks` | **Ninguno** | HPKE: DHKEM(P-256), HKDF-SHA256, AES-128-GCM |
| Transporte | QR, deeplink o DC API | QR o deeplink | Solo DC API |

Consecuencias:

- Un wallet que solo implemente el fallback de AV rechaza una petición firmada,
  y viceversa. El perfil no se negocia en tiempo de ejecución: el verifier tiene
  que mantener configuraciones separadas y elegir según el canal.
- La suite HPKE del anexo C viene fijada por la norma. Subirla (por ejemplo, a
  AES-256-GCM) rompe la interoperabilidad.
- Las versiones borrador de HAIP usaban otros esquemas (`x509_san_dns`,
  `verifier_attestation`). Un wallet construido sobre un borrador puede seguir
  esperándolos.

## 2. Los dos handovers de la DC API no son intercambiables (procedencia: norma)

El `SessionTranscript` del mdoc se construye distinto según el protocolo que se
use sobre la DC API:

```text
OpenID4VP sobre DC API (OpenID4VPDCAPIHandover):
  ["OpenID4VPDCAPIHandover", SHA-256(CBOR([origin, nonce, jwk_thumbprint]))]

ISO/IEC TS 18013-7 anexo C (org-iso-mdoc):
  [null, null, ["dcapi", SHA-256(CBOR([encryptionInfo_b64, origin]))]]
```

`jwk_thumbprint` es la huella RFC 7638 (SHA-256) de la clave de cifrado de la
respuesta. Si se construye el transcript de un protocolo con la fórmula del
otro, el fallo es opaco: error de etiqueta GCM al descifrar, o un error genérico
de CBOR. Hay que probarlo contra vectores fijos antes de usar un wallet real.

La fórmula de OpenID4VP está verificada contra OpenID4VP 1.0 final, B.2.6
(`OpenID4VPDCAPIHandoverInfo = [origin, nonce, jwkThumbprint]`). La del anexo
C de ISO/IEC TS 18013-7 está tomada de una implementación y queda sin
verificar contra la norma ISO, que es de pago.

## 3. DCQL para mdoc (procedencia: norma)

- En `mso_mdoc`, `meta` lleva **`doctype_value`**. No existe un campo `doctype`
  en DCQL.
- `credential_sets` es opcional. Con una sola credencial en `credentials[]`, su
  ausencia ya significa «pide esa credencial».
- `trusted_authorities` (tipo `etsi_tl`, entre otros) es parte de la
  especificación: dice al wallet qué emisores acepta el verifier.

## 4. Lo que se observa en la práctica (procedencia: observacion)

Medido en 2026 con wallets de verificación de edad y un verifier de código
abierto. No es norma y puede cambiar con cada versión:

- **Validadores estrictos.** Hay wallets que rechazan la petición entera si DCQL
  lleva un campo que la especificación no define (`meta.doctype`) o un campo
  opcional redundante (`credential_sets` con una sola credencial). Emitir solo
  lo mínimo es lo más interoperable.
- **`trusted_authorities` y wallets que no lo toleran.** Algún wallet de AV
  rechaza peticiones que lo incluyen. Si el verifier usa ese mismo campo para
  decidir en servidor contra qué lista valida al emisor, quitarlo de la
  petición no debe quitar la validación: la copia que se envía al wallet y la
  configuración con la que se valida tienen que ser independientes.
- **Ausencia de lista ≠ validación superada.** En algún verifier, una
  credencial cuya consulta no declara lista de confianza se da por buena sin
  comprobar el emisor. Hay que confirmar el comportamiento del verifier propio
  y tratar «sin lista» como error.
