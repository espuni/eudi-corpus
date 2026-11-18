---
id: CNF-008
titulo: "Perfil EUDI de emisión: OpenID4VCI según TS 119 472-3 y el anexo III de 2026/1731"
procedencia: mixta          # norma (§1-§6) · criterio (§7)
fuente: "ETSI TS 119 472-3 V1.1.1 (2026-03), aplicada por CIR 2024/2982 anexo I en la redacción de 2026/1731 (anexo XI); CIR 2024/2979 anexo Ib (2026/1731 anexo III)"
version_fuente: "TS 119 472-3 V1.1.1 (2026-03); textos oficiales vía inventario 300f644"
url: https://www.etsi.org/deliver/etsi_ts/119400_119499/11947203/01.01.01_60/ts_11947203v010101p.pdf
requisitos: ["GEN-REQ-4.1-01 a -06", "ISS-MDATA-4.2.1 a 4.2.3", "AUTH-REQ-4.4.2", "TOKEN-REQ-4.5", "CRED-REQ-4.6", "TR-WIA-1 a 4.3", "TR_KA-1 a 8", "LC_GEN-1 a 4"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [emision, openid4vci, haip, wia, ka, wua, grants, proof, metadatos]
relacionadas: [CNF-003, CNF-006, ARF-003, PRO-001, LEG-014, LEG-020]
---

# Perfil EUDI de emisión

## En una frase

La emisión de PID y EAA a la cartera es **OpenID4VCI perfilado por HAIP**, con
los cambios de ETSI TS 119 472-3. El acto 2026/1731 la hace obligatoria con
pocas adaptaciones y añade, en su anexo III, cómo se usan la WIA y la KA.

## 1. Qué obliga y en qué versión

- 2024/2982, anexo I (redacción de 2026/1731, anexo XI): se aplica **ETSI
  TS 119 472-3 V1.1.1 (2026-03)** con tres cambios:
  - **GEN-REQ-4.1-05 queda sin efecto**: ya no se exige presencia física
    para emitir PID con el flujo *pre-authorised code*;
  - el certificado de registro en `issuer_info` pasa de *may* a **shall**
    (ISS-MDATA-REG_CERT-4.2.3-04), y se eliminan los requisitos del
    `registrar_dataset` (4.2.3-07 a -13);
  - el anexo A de la TS (atestaciones X.509-AC) no se aplica.
- 2024/2979, anexo Ib (2026/1731, anexo III): la WUA, la WIA y la KA.

## 2. Recorrido de una emisión

| Paso | Qué ocurre | Requisito |
|---|---|---|
| Oferta | La cartera se invoca con el esquema **`eu-eaa-offer://`**. La oferta no va firmada | GEN-REQ-4.1-06 |
| Metadatos | El emisor publica **metadatos firmados** (JWS, OpenID4VCI 12.2.3), firmados con su **certificado de acceso**, que va en `x5c` junto con la cadena hasta el ancla sin incluirla. `issuer_info` va en el nivel superior y lleva su **certificado de registro** (`format: "registration_cert"`) | ISS-MDATA-4.2.1-01 y -02, ACC_CERT-4.2.2-01 a -03, REG_CERT-4.2.3-01 a -06 |
| PAR | La cartera envía la **WIA** como `OAuth-Client-Attestation` y su prueba de posesión | AUTH-REQ-4.4.2-01 y -02; TR-WIA-3 |
| Token | Otra vez la **WIA** con su prueba de posesión | TOKEN-REQ-4.5.1-01 y -02; TR-WIA-3 |
| Nonce | La cartera pide un `c_nonce` al *nonce endpoint* | CRED-REQ-4.6.1.2-02 |
| Petición de credencial | Si la credencial va ligada al dispositivo, `proofs` con la **KA**, como `jwt` o como `attestation` | CRED-REQ-4.6.1.1-01 y -02; TR_KA-3 |
| Emisión | Una credencial por cada clave de `attested_keys`, sin dos credenciales en la misma clave | CRED-REQ-PROC-4.6.2.1-04 a -06 |

Lo que **no** viaja: el certificado de acceso del emisor no va en la oferta,
sino en la firma de los metadatos. El emisor no se autentica en el PAR ni en
el token: lo hace con esos metadatos firmados.

## 3. Flujos (*grants*)

- El **emisor** implementa **al menos uno**: *authorisation code* o
  *pre-authorised code* (GEN-REQ-4.1-04; ISS-CRED-OFFER-4.3-01).
- La **cartera** implementa **los dos** (GEN-REQ-4.1-03).
- Emitir PID solo con *pre-authorised code* es conforme: el requisito de
  presencia física (GEN-REQ-4.1-05) lo anula 2026/1731.
- Los *refresh tokens* para renovar credenciales son opcionales
  (TOKEN-REQ-PROC-4.5.2-04).

## 4. WIA y KA: qué demuestra cada una y qué comprueba el emisor

**Vocabulario.** Para 2026/1731, la WUA comprende una o varias WIA y una o
varias KA. TS 119 472-3 llama «WUA» a lo que va en `key_attestation`, es decir,
a la KA (CRED-REQ-4.6.1.2-04 y -05). Al citar, hay que precisar cuál.

| | WIA | KA |
|---|---|---|
| Qué demuestra | Que la instancia de cartera es auténtica e íntegra: el proveedor verificó la integridad menos de 24 h antes de su `exp` | Que las claves del titular están en el WSCD o el almacén de claves descrito |
| Cuándo se usa | En toda emisión de PID, QEAA, EAA o PuB-EAA | En la emisión de PID y de atestaciones **ligadas al dispositivo**. **No** se usa si la atestación no va ligada al dispositivo |
| Dónde va | PAR y token | Petición de credencial (`proofs`) |
| Reutilización | Una WIA a un solo servidor de autorización; con la opción *per-issuer reuse*, varias veces al mismo | Una KA en un solo proceso de emisión |
| Requisitos | TR-WIA-1, -2.1, -3, -3.2 | TR_KA-1, -1.1, -2.4, -3 |

Lo que comprueba el emisor:

- **WIA**: la firma con el certificado del `x5c`; que ese certificado llega a
  un ancla de la **lista de proveedores de cartera** (2024/2980 art. 5); que no
  ha caducado; y la prueba de posesión con la clave del `cnf` (TR-WIA-4 a 4.3).
- **KA**: la firma con el certificado del `x5c` y su cadena hasta la misma
  lista (TR_KA-5). En la prueba `jwt`, además, la firma del elemento con la
  clave de la posición 0 de `attested_keys` y que el `nonce` es un `c_nonce`
  válido (TR_KA-6 y 6.1). En la prueba `attestation`, que la KA lleva un
  `c_nonce` válido (TR_KA-7).

## 5. Tipos de prueba y vínculo con el dispositivo

- La cartera elige `jwt` **o** `attestation` (CRED-REQ-4.6.1.1-02).
- El emisor de credenciales ligadas al dispositivo anuncia en
  `proof_types_supported` que admite **los dos**, con `key_attestations_required`
  (TR_KA-4). Admitir solo `jwt` no cumple.
- Si la credencial no va ligada al dispositivo, el emisor **omite**
  `proof_types_supported` y `cryptographic_binding_methods_supported`
  (TR_KA-4.1).
- El **PID** se liga siempre a una clave de una KA que mencione un **WSCD**
  (TR_KA-8).

## 6. Estado de la WIA y la KA, y su efecto en el PID

- La cartera debe poder presentar siempre WIA y KA cuyo
  `client_status.exp` y `key_storage_status.exp` estén al menos **31 días** en
  el futuro (LC_GEN-1).
- La validez técnica del PID termina **antes** que esos dos plazos (LC_GEN-3).
- Un PID válido más de 24 h obliga a su proveedor a comprobar **cada 24 h** el
  estado de la WIA y la KA recibidas en la emisión (LC_GEN-4). Si están
  revocadas, revoca el PID (2024/2977 art. 5.4.b).
- El `exp` de la WIA **no** marca el fin del periodo en que se mantiene su
  estado de revocación (LC_WIA_2).

## 7. Lo que conviene tener claro (procedencia: criterio)

- **Presentación durante la emisión.** Ni TS 119 472-3 ni los actos regulan
  que el emisor pida una presentación (por ejemplo, del PID) dentro de la
  emisión. Lo que sí prevé el ARF es que un proveedor de atestaciones que
  necesite datos del usuario se registre **también como parte usuaria** y los
  pida con una presentación normal (ARF 6.3.2.3). Quien presenta es la
  cartera; el emisor actúa como verificador, no al revés.
- **Cifrado.** Además de las suites de HAIP, cartera y emisor admiten
  A128GCM y A256GCM (CRYPTO-5-01).
- **Lo que viene de HAIP y no repite la TS**: PKCE con S256, **DPoP**, `scope`
  por configuración de credencial y *nonce endpoint* obligatorio si hay
  credenciales ligadas a clave (HAIP 4 y 4.1). Ver
  [PRO-003](../protocolos/haip.md).
