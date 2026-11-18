---
id: PRO-002
titulo: "OpenID4VP 1.0: anatomía de una presentación"
procedencia: norma
fuente: "OpenID for Verifiable Presentations 1.0, final (2025-07-09)"
version_fuente: "OpenID4VP 1.0 final, 2025-07-09"
url: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html
requisitos: ["OpenID4VP §5.1, §5.2, §5.9.3, §5.11", "§8.1 a §8.6", "§14.1", "apéndice A", "apéndice B.2"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [openid4vp, presentacion, dcql, direct-post, dc-api, cifrado, vp-token]
relacionadas: [PRO-004, PRO-003, CNF-007, PRO-010]
---

# OpenID4VP 1.0: anatomía de una presentación

## En una frase

El verificador pide con una **consulta DCQL** y un **nonce**; la cartera
devuelve un **`vp_token`** con una presentación por cada consulta, ligada al
`client_id` y al nonce de esa petición; el verificador la valida entera.

El perfil EUDI que se apoya en esto está en
[CNF-007](../confianza/perfil-presentacion.md) y [PRO-003](haip.md).

## 1. La petición

| Parámetro | Qué es | Referencia |
|---|---|---|
| `client_id` | Identificador del verificador, con prefijo (`x509_hash:`, `redirect_uri:`…). Con `x509_hash`, es el SHA-256 del certificado hoja en base64url, y la petición va firmada con su clave | §5.2, §5.9.3 |
| `response_type` | `vp_token` | §5.6 |
| `response_mode` | **Obligatorio.** `direct_post`, `direct_post.jwt` (cifrada), `dc_api`, `dc_api.jwt` | §5.2, §8.2, §8.3, apéndice A |
| `nonce` | **Obligatorio.** Aleatorio y nuevo en cada petición; ata la presentación a la transacción | §5.2 |
| `dcql_query` | La consulta. Va esto **o** un `scope` que represente una consulta, nunca los dos | §5.1, §6 |
| `client_metadata` | Metadatos del verificador: `jwks` para cifrar la respuesta, `encrypted_response_enc_values_supported`, `vp_formats_supported` | §5.1 |
| `verifier_info` | Atestaciones sobre el verificador (`format`, `data`, `credential_ids` opcional). La cartera decide si las usa; el perfil EUDI mete aquí el certificado de registro | §5.1, §5.11 |
| `transaction_data` | Datos de una transacción que el usuario autoriza (pago, firma). Si la cartera no los admite, **devuelve error** | §5.1, §8.4 |
| `request_uri`, `request_uri_method` | Petición por referencia, por GET o POST | §5.10 |
| `state` | Opcional salvo en presentaciones sin vínculo con el titular | §5.2, §5.3 |

## 2. La respuesta

- `vp_token` es un objeto JSON: la clave es el `id` de cada consulta DCQL y el
  valor, una lista de presentaciones. Sin `multiple: true`, una sola (§8.1).
- **Cifrado** (§8.3): JWT sin firmar y cifrado (JWE) con una clave de
  `client_metadata.jwks`. El `alg` del JWE es el de la clave elegida; el `enc`
  sale de `encrypted_response_enc_values_supported` (A128GCM por defecto), y si
  la clave tiene `kid`, el JWE lo repite.
- **Errores** (§8.5): `invalid_request` (consulta y `scope` a la vez, prefijo
  de cliente no admitido…), `invalid_client`, `access_denied` (sin
  credenciales, sin consentimiento o sin autenticar al usuario),
  `vp_formats_not_supported`, `invalid_request_uri_method`,
  `invalid_transaction_data` y `wallet_unavailable`.

## 3. Qué valida el verificador (§8.6 y §14.1)

1. El formato del `vp_token`.
2. Para cada presentación: integridad y autenticidad de la presentación y de
   la credencial.
3. Que la credencial cumple los criterios de la consulta.
4. Que hay prueba de vínculo con el titular, salvo que se pidiera sin ella.
5. Ese vínculo, incluidas las comprobaciones contra repetición: la prueba está
   ligada al `client_id` y al `nonce` de la petición.
6. Las comprobaciones de su política de confianza, como la revocación.
7. Que el conjunto devuelto cumple la consulta entera.

Si falla una presentación, se descarta; si falla algo del conjunto, se rechaza
el `vp_token` entero.

## 4. Por la Digital Credentials API (apéndice A)

La petición se entrega por `navigator.credentials.get()`. La audiencia de la
presentación es siempre el origen con el prefijo `origin:`, que la cartera no
acepta como prefijo en una petición normal (§5.9.3). Para mdoc, el
`SessionTranscript` usa `OpenID4VPDCAPIHandover`, calculado sobre
`[origin, nonce, jwkThumbprint]` (B.2.6).

## 5. Presentaciones sin vínculo con el titular (§5.3 y §14.1.1)

Se pueden pedir con `require_cryptographic_holder_binding: false`, pero no
protegen contra la repetición: quien las acepta asume que el presentador puede
no ser el titular.
