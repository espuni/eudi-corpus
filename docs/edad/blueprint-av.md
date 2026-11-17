---
id: AV-001
titulo: "EU Age Verification Blueprint: roles, modelo de datos, emisión y modelo de confianza"
procedencia: mixta          # norma (§1-§5) · criterio (§6)
fuente: "av-doc-technical-specification, rama main, commit 8b97287 (2026-09-02)"
version_fuente: "commit 8b97287; la última etiqueta, v1.0.6, es de julio de 2025 y está superada"
url: https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/architecture-and-technical-specifications.md
requisitos: ["Spec. principal §2.2.3, §2.6, §3.4.1-§3.4.4, §4.2-§4.5", "Anexo A §A.3-§A.5"]
estado: borrador
verificado: 2026-11-17
revisar_antes: 2027-03-01
tags: [verificacion-de-edad, blueprint, mdoc, emision, confianza]
relacionadas: [AV-002, AV-003, LEG-030, LEG-031, FMT-001]
---

# EU Age Verification Blueprint

## En una frase

Solución de la Comisión para verificar la edad en línea conforme al art. 28 del
DSA, construida con los protocolos de la cartera EUDI pero con un perfil propio
más simple: atestación mdoc de un solo atributo, sin registro de partes usuarias
y con la confianza anclada solo en una Trusted List de emisores.

## 1. Documentos y versión

- Especificación principal: *Operational, Security, Product, and Architecture
  Specifications* ([texto](https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/architecture-and-technical-specifications.md)).
- Anexo A, perfil normativo de interoperabilidad
  ([texto](https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/annexes/annex-A/annex-A-av-profile.md)).
- Anexo B, pruebas de conocimiento cero ([texto](https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/annexes/annex-B/annex-B-zkp.md)).

**Cuidado con la versión.** El repositorio no etiqueta versiones desde la
v1.0.6 (julio de 2025); la rama `main` ha cambiado mucho desde entonces (entre
otras cosas, la prueba ZK pasó a ser el mecanismo preferido). Citar siempre el
commit.

## 2. Roles

| Rol | Qué hace |
|---|---|
| Attestation Provider (AP) | Identifica al usuario y emite la atestación de edad. Figura en la Trusted List |
| Age Verification App (AVI) | La app del usuario: guarda las atestaciones y las presenta |
| Relying Party (RP) | El servicio que pide la prueba de edad |
| Comisión | Opera la Trusted List de AP y la lista de apps conformes |

## 3. Modelo de datos (anexo A §A.4)

- Formato: **solo mdoc** (ISO/IEC 18013-5 e ISO/IEC 23220-2).
- docType y namespace: **`eu.europa.ec.av.1`**.
- Atributos: `age_over_18` (obligatorio en la emisión) y, opcionalmente,
  `age_over_NN` con otros umbrales. **Ningún otro atributo.**
- En la verificación se pide **uno**: `age_over_18` o un `age_over_NN`.
- El perfil se centra en 18; otros umbrales exigen validar el método de
  alta para ese grupo de edad y su base jurídica.

## 4. Emisión y ciclo de vida

- **OpenID4VCI**, siguiendo el marco de emisión de la cartera EUDI (§A.5,
  *SHOULD*). Un AP y un proveedor de app pueden acordar una interfaz interna si
  logra garantías equivalentes.
- **Invocación de la app para la oferta:** al menos el esquema `av-vci://`
  (*MUST*, §A.5). Los ejemplos del propio anexo usan `av://` para la oferta:
  incoherencia del documento; lo normativo es `av-vci://`.
- **Identificador de configuración:** los ejemplos usan `proof_of_age`, pero
  el texto normativo no lo exige.
- **AVS Unit Attestation (AVSUA):** la app *SHOULD* presentar al AP una
  atestación de instancia (AVIA) y una de clave (KA), firmadas por el proveedor
  de la app. Es la WUA de TS03 aplicada a AV: AVIA ↔ WIA, KA ↔ KA.
- **Lotes:** el AP *SHALL* admitir emisión por lotes; se recomiendan **30**
  atestaciones, con las horas de `ValidityInfo` igualadas para limitar la
  vinculabilidad (§3.4.1).
- **Un solo uso** en presentación mdoc simple; una prueba ZK *MAY* reutilizarse
  dentro de su validez (§3.4.3).
- **Validez** recomendada de **3 meses** como máximo; nueva identificación del
  usuario al menos cada 3 meses (§3.4.2-§3.4.3).
- **Sin revocación ni reemisión** en esta versión (§2.2.3, §3.4.3). Si hiciera
  falta, se apunta a una status list.
- **Nivel de garantía:** sustancial. El nivel alto está fuera de alcance (§A.3).

## 5. Modelo de confianza (§3.4.4, §4.4, §4.5)

- La confianza se ancla en una **Trusted List de AP** (ETSI TS 119 612) que
  opera la Comisión y publica el eIDAS Dashboard. Detalle en
  [AV-003](trusted-list-av.md).
- El certificado firmante del AP sigue ETSI EN 319 411-1, política **NCP**,
  expedido por un QTSP o por una CA propia del AP.
- **No hay registro de partes usuarias ni de proveedores de app**, ni
  certificados de acceso. La RP se autentica solo con TLS/Web PKI.
- La confianza en la app se establece **en la emisión**: el AP comprueba que la
  app es genuina (AVSUA o mecanismo equivalente) antes de emitir.
- Requisitos de la RP (§4.4): implementar el anexo A; **verificar pruebas ZK** y
  aceptar el fallback mdoc; validar autenticidad e integridad; comprobar contra
  la Trusted List que el AP está autorizado; comprobar que viene el atributo
  pedido.

## 6. Límites del diseño (procedencia: criterio)

Lecturas propias del diseño, no afirmaciones de la especificación:

- **Ninguna autenticación de la RP ante la app.** Cualquier web puede pedir la
  prueba. El daño es acotado (un booleano), pero abre la puerta a pedir la
  verificación sin necesidad y a ataques de reenvío del QR.
- **Sin revocación**, una atestación vale hasta su caducidad pase lo que pase;
  la única frescura es la validez corta. Conviene decírselo a la RP.
- **Proximidad en cross-device** sin mecanismo especificado: el reenvío del QR
  (phishing) queda abierto; un tiempo de vida corto de la sesión lo mitiga.
- **Fragmentación:** «app de marca blanca + adaptaciones nacionales» implica
  variantes por país desde el primer día. Hay que probar cada app nacional.
- **Uso por la RP:** pedir la prueba en cada acceso agota el lote. El patrón
  razonable es verificar una vez y recordar el resultado en la cuenta del
  usuario (por ejemplo, con una passkey).
