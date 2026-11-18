---
id: CNF-003
titulo: "Certificados de acceso (WRPAC) y de registro (WRPRC): qué es cada uno y qué comprueba la cartera"
procedencia: mixta          # norma (§1-§3) · criterio (§4)
fuente: "CIR 2025/848 modificado por 2026/1730; CIR 2024/2982 modificado por 2026/1731; ARF v3.0.0 3.18, 3.19, 6.3.2.3; ETSI TS 119 411-8 V1.1.1; ETSI TS 119 475 V1.2.1"
version_fuente: "textos oficiales vía inventario 300f644; ARF v3.0.0"
url: https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v3.0.0/docs/main/03-roles-within-the-eudi-wallet-ecosystem.md
requisitos: ["2025/848 art. 7 y 8", "2026/1730 art. 1.4", "2024/2982 art. 3 y 8 (redacción de 2026/1731)", "ARF 3.18, 3.19", "TS 119 411-8 OVR-4.2.2-02", "TS 119 475 cl. 4.4, GEN-5.2.1-01 a -03"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [wrpac, wrprc, parte-usuaria, registro, over-asking, confianza]
relacionadas: [ARF-001, CNF-009, PRO-010, LEG-017, LEG-019]
---

# Certificados de acceso y de registro

## En una frase

El **certificado de acceso** (WRPAC) autentica a quien se conecta con la
cartera; el **certificado de registro** (WRPRC) dice qué está registrado para
pedir o emitir. La cartera tiene que validar el primero siempre, y el segundo
solo desde el **11 de agosto de 2028**.

## 1. Las diferencias

| | Certificado de acceso (WRPAC) | Certificado de registro (WRPRC) |
|---|---|---|
| Qué es | Certificado X.509 (RFC 5280, ETSI TS 119 411-8), con política NCP como mínimo (OVR-4.2.2-02) | **JWT o CWT** firmado, con `typ` `rc-wrp+jwt` o `rc-wrp+cwt` y firma AdES B-B (TS 119 475, cl. 4.4 y GEN-5.2.1-01). **No** es un certificado X.509. El ARF solo menciona el JWT (3.19) |
| Quién lo expide | Una CA que el Estado autoriza: al menos una, obligatorio (2025/848 art. 7.1) | Un proveedor que el Estado autoriza. Era opcional y es obligatorio desde 2026/1730, que además exige emitirlo de forma automatizada y sin demora tras el registro |
| A quién | Solo a partes usuarias registradas (art. 7.2). Un certificado por instancia técnica (ARF 3.18) | Solo a partes usuarias registradas (art. 8.2.a) |
| Qué contiene | La identidad técnica | Cada uso previsto (art. 8.2.b), la política general de acceso (8.2.c) y la URL de la política de privacidad (8.2.g y 8.3) |
| Para qué sirve | Que la cartera sepa con quién habla y valide la petición | Que la cartera compruebe que lo pedido o lo emitido está dentro de lo registrado |
| Cómo se enlazan | Ambos llevan el identificador único de la entidad y el de su servicio (ARF 3.19) | |
| Dónde está la confianza | LoTE de Access CA | LoTE de proveedores de certificados de registro |

Los **emisores** también los tienen. Los proveedores de PID y de atestaciones
se registran, reciben los dos certificados y los publican en sus metadatos
OpenID4VCI (ARF 6.3.2.3). El certificado de acceso de un emisor **no** dice si
es de PID, QEAA o PuB-EAA: eso va en el de registro. Un emisor que además pide
datos (por ejemplo, el PID durante la emisión) se registra con los dos roles.

## 2. Qué tiene que hacer la cartera (2024/2982 art. 3)

En la redacción de 2026/1731, las unidades de cartera:

1. autentican y validan el certificado de acceso al interactuar con una parte
   usuaria, **sin delegarlo** en el navegador del sistema operativo ni en otra
   aplicación intermedia (art. 3.1);
2. autentican y validan las peticiones hechas con ese certificado (art. 3.3);
3. autentican y validan el certificado de registro (art. 3.4), **solo desde el
   11 de agosto de 2028** (art. 8, en su nueva redacción);
4. muestran al usuario la información del certificado de acceso (art. 3.5);
5. no presentan ningún atributo hasta haber procesado las políticas de
   divulgación incrustadas y tener la aprobación del usuario (art. 3.9).

## 3. Pedir de más (*over-asking*)

La base está en 2025/848:

- el certificado de registro lleva una política general de acceso, armonizada
  en toda la Unión, que informa al usuario de que la parte usuaria solo puede
  pedir lo que figura en el certificado para el uso registrado (art. 8.2.c);
- los proveedores de cartera cumplen esa política **avisando al usuario**
  cuando una parte usuaria pide datos que no están en el certificado
  (art. 8.2.d).

## 4. Lo que conviene tener claro (procedencia: criterio)

- **Hasta agosto de 2028 la comprobación de pedir de más no es exigible a la
  cartera**, porque depende de validar el certificado de registro. Una cartera
  puede hacerla antes, pero una parte usuaria no puede contar con ello.
- **Ambigüedad de fechas.** El acto aplaza a 2028 solo el **art. 3.4** de
  2024/2982 (validar el certificado de registro). Los requisitos
  WRP-VALIDATION-01 y -02 y WRP-OVERASKING-01 a -03 están en el **anexo II** del
  mismo reglamento, al que remite su art. 5, y el acto **no los aplaza
  expresamente**. El considerando 6 de 2026/1731 dice que la intención es que
  esa obligación se aplique desde el 11-8-2028. Criterio: tratarlo como
  exigible en 2028, pero implementarlo antes, porque una lectura literal del
  anexo podría exigirlo ya.
- **JWT o CWT.** TS 119 475 admite los dos; el ARF solo habla del JWT. Para
  pedir datos por OpenID4VP el caso que importa es el JWT; el CWT tiene
  sentido en flujos CBOR (mdoc).
- **TS 119 475 V1.2.1 va por detrás de 2026/1730.** Todavía dice que los
  Estados «may mandate or allow» los certificados de registro y que, si no se
  emite uno, la cartera consulta el registro nacional (cl. 4.4). Desde
  2026/1730 los Estados **deben** autorizar al menos un proveedor; el acto
  prevalece sobre la TS.
- **El formato JWT tiene una consecuencia práctica**: no se valida con una
  biblioteca X.509, sino como un JWS cuya clave encadena hasta la LoTE de
  proveedores de certificados de registro.
