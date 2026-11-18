---
id: AV-004
titulo: "Pruebas de conocimiento cero en verificación de edad: el esquema longfellow"
procedencia: mixta          # norma (§1-§3) · observacion (§4) · criterio (§5)
fuente: "av-doc-technical-specification, anexo A §A.8 y anexo B (commit 8b97287); ARF TS04, TS13 y TS14"
version_fuente: "commit 8b97287 (2026-09-02); anexo B actualizado a 07/2026"
url: https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/annexes/annex-B/annex-B-zkp.md
requisitos: ["AV anexo A §A.8", "AV anexo B §B.2, §B.3, §B.4"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-03-01
tags: [zk, longfellow, verificacion-de-edad, mdoc, dc-api, privacidad]
relacionadas: [AV-002, AV-001, OBS-001, ARF-006]
---

# Pruebas de conocimiento cero: el esquema longfellow

## En una frase

La app demuestra, sin enseñar la atestación, que tiene una atestación de edad
válida, firmada por un emisor de la lista, con el atributo pedido a `true` y
ligada a su clave. El emisor no cambia nada: la prueba se construye sobre el
mdoc normal firmado con ECDSA.

## 1. El esquema (anexo B, §B.2)

- **«Anonymous credentials from ECDSA»** (Frigo y shelat), sobre el
  protocolo Ligero. **No necesita configuración de confianza** previa
  (*trusted setup*).
- Se basa en un **circuito aritmético**:
  - entrada secreta: la atestación de edad;
  - entradas públicas: la clave pública del emisor, el atributo y el nonce;
  - devuelve `true` si la firma del emisor es válida, el atributo es `true`, la
    app firma el nonce con la clave de la atestación y la atestación está
    dentro de su validez.
- **Emisión sin cambios**: el emisor ni siquiera sabe que se usará.

## 2. Por qué este y no otro (anexo B, §B.3, evaluación de junio de 2025)

Se compararon cinco esquemas: BBS+, BBS+ con prueba de posesión ECDSA, BBS+ sin
emparejamientos, credenciales anónimas ECDSA y Crescent. Ganó el de credenciales
anónimas ECDSA porque **no obliga a cambiar la infraestructura**: sirve con
los formatos de credencial y los flujos de emisión que ya existen. Las
variantes de BBS+ exigían emisores nuevos.

## 3. Estado a julio de 2026 (anexo B, §B.4)

- **Revisado**: auditorías de Trail of Bits (agosto de 2025) e ISRG (octubre
  de 2025), y un panel académico reunido por Ligero (diciembre de 2025). Las
  dos auditorías encontraron fallos en el circuito mdoc (variables del testigo
  sin restringir lo suficiente, que afectaban a la solidez), ya corregidos; el
  de ISRG, en la versión 0.8.4.
- **Publicado con revisión por pares**: IACR Communications in Cryptology,
  vol. 3, n.º 1, 4 de mayo de 2026. Con eso se da por cumplido el requisito de
  revisión por pares (Req02).
- **Sin estándar**: hay un borrador individual en el IETF
  (`draft-google-cfrg-libzk`) que el grupo CFRG no ha adoptado.
- **Implementaciones**: la de referencia en C++ (probada con la v0.9, de 31 de
  marzo de 2026) y una en Rust de ISRG, compatible bit a bit.
- **Plataformas**: iOS desde la versión 27 y Android desde la 10.
- **Despliegues**: Google Wallet (con Bumble), y carteras EUDI como wwWallet y
  Multipaz lo están integrando.

Lo normativo para la parte usuaria está en el anexo A §A.8
([AV-002](perfil-presentacion-av.md)): un solo sistema (`longfellow-libzk-v1`),
estructura `ZkSystemSpec` de ISO/IEC 18013-5 2.ª edición, comprobación del hash
del circuito contra la lista de circuitos aceptados **antes** de verificar, y
aceptación obligatoria del mdoc simple como alternativa.

## 4. Lo observado en la práctica (procedencia: observacion)

- Una prueba ocupa unos **360 KB** y se verifica en menos de un segundo en
  servidor.
- En cross-device por la DC API, la prueba **no vuelve** por el túnel CTAP
  *hybrid* ([OBS-001](../observaciones/zk-cross-device.md)). El perfil EUDI ya
  prefiere CTAP 2.3 sobre BLE para cross-device
  ([CNF-007](../confianza/perfil-presentacion.md)).

## 5. Lo que conviene tener claro (procedencia: criterio)

- **El ancla de confianza no viaja igual.** En un mdoc normal el verificador ve
  el certificado del firmante y lo encadena a la lista. En la prueba ZK, la
  clave pública del emisor es una entrada pública del circuito: el verificador
  tiene que saber **contra qué claves** comprueba, y esas claves salen de la
  Trusted List de AV.
- **La lista de circuitos aceptados es una dependencia operativa nueva**: la
  publica el responsable del esquema, fuera de la especificación, y hay que
  seguirla igual que la Trusted List.
- **EUDI.** Las especificaciones técnicas de la Comisión TS04, TS13 y TS14
  tratan las pruebas de conocimiento cero en la cartera EUDI (ver
  [ARF-006](../arf/especificaciones-tecnicas.md)). No se han contrastado aquí
  con el perfil de AV.
