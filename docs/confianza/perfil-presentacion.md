---
id: CNF-007
titulo: "Perfil EUDI de presentación: TS 119 472-2 y el anexo XII de 2026/1731"
procedencia: mixta          # norma (§1-§5) · criterio (§6)
fuente: "ETSI TS 119 472-2 V1.2.1 (2026-03) e ISO/IEC 18013-7:2025 anexo C, aplicados por CIR 2024/2982 anexo II en la redacción de 2026/1731 (anexo XII)"
version_fuente: "TS 119 472-2 V1.2.1 (2026-03); textos oficiales vía inventario 300f644"
url: https://www.etsi.org/deliver/etsi_ts/119400_119499/11947202/01.02.01_60/ts_11947202v010201p.pdf
requisitos: ["WRP-VALIDATION-01 a -03", "WRP-OVERASKING-01 a -03", "EAAP-API-GEN-01 y -02", "ISO/IEC 18013-5-REQ-04 a -07", "ISO/IEC 18013-SUPPORT-01 y -04", "OIDFVP-HAIP-SUPPORT", "OIDFVP-HAIP-COMMON-REQ-RO-13 a -23", "OIDFVP-HAIP-ADD-API-05"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [presentacion, openid4vp, haip, dcql, dc-api, mdoc, wrpac, wrprc, over-asking]
relacionadas: [CNF-003, CNF-006, PRO-010, OBS-001, PRO-002, LEG-014, LEG-020]
---

# Perfil EUDI de presentación

## En una frase

Hay dos perfiles: **mdoc** (ISO 18013-5 en proximidad, ISO 18013-7 anexo C por
la API del navegador) y **OpenID4VP perfilado por HAIP** (por redirección o por
la API). En los dos, la cartera recibe el certificado de registro de la parte
usuaria, lo valida y avisa si pide de más.

## 1. Qué obliga, y qué cambió el acto respecto a la TS

2024/2982, anexo II (redacción de 2026/1731, anexo XII): se aplican
ISO/IEC 18013-7:2025 anexo C y las cláusulas 4.1, 4.2, 5 y 6 de **ETSI
TS 119 472-2 V1.2.1 (2026-03)**, con adaptaciones. Las que más cambian la TS:

| Requisito de la TS | Qué decía | Tras 2026/1731 |
|---|---|---|
| OIDFVP-HAIP-COMMON-REQ-01 | Prefijo de cliente `x509_hash` obligatorio | **Sin efecto** como requisito propio; HAIP 5 lo sigue exigiendo para peticiones firmadas |
| RO-01 a RO-12 | `verifier_info` con `registrar_dataset` | **Sin efecto** |
| RO-13 | El certificado de registro en `verifier_info` «si la parte usuaria lo tiene» | **Siempre**: un elemento de `verifier_info` incluye el certificado de registro |
| RO-23 | La petición la firma la clave del certificado de acceso | Con `x509_hash`, el certificado hoja es el certificado de acceso |
| COMMON-RESP-01 | La cartera cifra la respuesta | **Sin efecto** como requisito propio; HAIP 5 sigue exigiendo el cifrado |
| REDIRECTS-04 | Petición por referencia (`request_uri`) obligatoria | **Sin efecto**; HAIP 5.1 sigue exigiendo JAR con `request_uri` |
| SUPPORT-02 y -05 | La API (DC API) era opcional | **Obligatoria** para la cartera y para la parte usuaria |
| SUPPORT-03 | Cross-device solo por la API | La cartera **no debería** admitir el mecanismo por redirección en cross-device: es vulnerable a fijación de sesión |
| ADD-API-05 | CTAP 2.2 *hybrid* para cross-device | Comprobar **proximidad física** por un canal local; se prefiere CTAP 2.3 sobre BLE frente al túnel *hybrid* |

Se mantiene, entre otros:

- RO-14 a RO-16: el elemento de `verifier_info` con el certificado de registro
  lleva `format: "registration_cert"` y el certificado en base64url, y no
  lleva `credential_ids`;
- RO-18 a RO-22: `client_metadata` con `jwks` (`kid` y `use`) y `aud`;
- API-03: la cartera no admite `openid4vp-1-unsigned`.

## 2. Comprobaciones de la cartera sobre la parte usuaria

Nueva cláusula 4.4, introducida por 2026/1731:

- **Validar el certificado de registro** antes de mostrar nada al usuario
  (WRP-VALIDATION-01). Si falla (caducado, revocado, de un proveedor no
  reconocido, mal formado o con firma inválida), la cartera **avisa**, no
  presenta la petición como validada y exige aprobación explícita: el
  silencio o las casillas premarcadas no valen (WRP-VALIDATION-02). El
  proveedor de cartera decide qué fallos puede saltarse el usuario
  (WRP-VALIDATION-03).
- **Pedir de más.** La cartera compara lo pedido con lo registrado
  (WRP-OVERASKING-01). Si se pide más, avisa antes de revelar nada y exige
  aprobación explícita (-02). El proveedor de cartera decide si se puede
  continuar, si solo se revela lo cubierto o si se rechaza (-03).

Recordatorio de fechas: la obligación de validar el certificado de registro
(2024/2982 art. 3.4) aplica **desde el 11 de agosto de 2028**.

## 3. Perfil mdoc

- **Prohibida la recuperación en servidor** de ISO 18013-5 (ISO/IEC
  18013-SUPPORT-01).
- La parte usuaria **debería** implementar el perfil de la API, es decir,
  ISO 18013-7 anexo C (SUPPORT-04).
- La petición lleva `requestInfo` con el miembro **`euWrprc`**: el certificado
  de registro **codificado en CBOR** (18013-5-REQ-04 a -07).
- Las claves de la credencial no firman datos aportados por la parte usuaria,
  salvo los datos de transacción previstos (18013-5-RESP-02 y -03).

## 4. La API del navegador (DC API)

- La cartera admite la API para **los dos** protocolos: OpenID4VP (HAIP 5.2)
  e ISO 18013-7 anexo C (EAAP-API-GEN-01), al menos para los tipos del
  catálogo y los formatos del anexo II de 2024/2979 (-02). Si el sistema
  operativo o el navegador lo impiden, la no conformidad se atribuye a ellos.
- La cartera anuncia a la API **qué tipos** de atestación guarda, pero no sus
  atributos ni sus valores, y el usuario puede desactivarlo
  (ADD-API-01 a -04).

## 5. OpenID4VP

- Se aplican los requisitos obligatorios de HAIP 5, 5.3, 7 y 8
  (OIDFVP-HAIP-GEN-01). Por redirección se añade HAIP 5.1; por la API, HAIP 5.2.
- Para mdoc, el perfil «ISO mdocs» de HAIP; para SD-JWT VC, el perfil «IETF
  SD-JWT VCs» (GEN-04 y -05).
- La consulta es **DCQL** (OpenID4VP 1.0, cláusula 6).

## 6. Lo que conviene tener claro (procedencia: criterio)

- **Las anulaciones no relajan el perfil.** `x509_hash`, el cifrado de la
  respuesta y la petición por referencia ya no obligan **por la TS**, pero
  HAIP 5 y 5.1 los siguen exigiendo y el acto aplica HAIP (ver
  [PRO-003](../protocolos/haip.md)). Lo único que desaparece de verdad es el
  `registrar_dataset`. Antes de citar un requisito de la TS, hay que mirar si
  el anexo XII lo anula y, si lo hace, citar HAIP en su lugar.
- **Peticiones sin firmar por la DC API.** HAIP 5.2 obliga a la cartera a
  admitirlas; TS 119 472-2 API-03 se lo prohíbe, y prevalece la TS
  (OIDFVP-HAIP-GEN-03).
- **Posible errata del acto.** El RO-23 adaptado dice que el certificado de
  acceso es el especificado «en ETSI TS 119 475». El perfil del certificado de
  acceso es TS 119 411-8; TS 119 475 trata del registro.
- **Cross-device y pruebas grandes.** La preferencia por CTAP 2.3 sobre el
  túnel *hybrid* casa con lo observado: una prueba ZK de cientos de KB no
  vuelve por el túnel (ver [OBS-001](../observaciones/zk-cross-device.md)).
