---
id: CNF-009
titulo: "Mapa de listas: qué Trusted List o LoTE ancla a cada actor"
procedencia: mixta          # norma (§1-§2) · criterio (§3)
fuente: "CIR 2024/2980 art. 5 (redacción de 2026/1731); eIDAS art. 22 y 45f.3; ARF v3.0.0 3.5, 6.2.2, 6.2.3, 6.3.2.4, 6.3.3"
version_fuente: "textos oficiales vía inventario 300f644; ARF v3.0.0"
url: https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v3.0.0/docs/main/03-roles-within-the-eudi-wallet-ecosystem.md
requisitos: ["2024/2980 art. 5.1 y 5.2", "eIDAS art. 22", "eIDAS art. 45f.3", "ARF 3.5", "ARF 6.3.2.4"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [trusted-list, lote, anclas, confianza, listas]
relacionadas: [ARF-001, CNF-003, CNF-001, CNF-002, ARF-003, AV-003]
---

# Mapa de listas y anclas de confianza

## En una frase

Solo el proveedor de QEAA se ancla en una **Trusted List** nacional
(ETSI TS 119 612). El resto de actores con lista se anclan en una **LoTE**
(ETSI TS 119 602), que firma y publica la Comisión. Las partes usuarias no
tienen lista.

## 1. Las listas

| Lista | Formato | Quién la publica | A quién recoge | Base | Quién la consulta y para qué |
|---|---|---|---|---|---|
| Trusted List nacional | TS 119 612 | Cada Estado | QTSP, entre ellos los proveedores de QEAA | eIDAS art. 22 | Parte usuaria: validar una QEAA y su lista de estado |
| LoTE de proveedores de cartera | TS 119 602 | Comisión | Proveedores de cartera | 2024/2980 art. 5.2 | Emisor: validar la WIA, la KA y sus listas de estado (ARF 6.2.2) |
| LoTE de proveedores de PID | TS 119 602 | Comisión | Proveedores de PID | 2024/2980 art. 5.2 | Parte usuaria: validar el PID y su estado |
| LoTE de organismos PuB-EAA | TS 119 602 | Comisión | Organismos que expiden PuB-EAA | eIDAS art. 45f.3 | Parte usuaria: validar una PuB-EAA |
| LoTE de Access CA | TS 119 602 | Comisión | Proveedores de certificados de acceso | 2024/2980 art. 5.2 | Cartera: validar el certificado de acceso de emisores y partes usuarias |
| LoTE de proveedores de certificados de registro | TS 119 602 | Comisión | Proveedores de certificados de registro | 2024/2980 art. 5.2 (añadida por 2026/1731) | Cartera: validar el certificado de registro |
| Lista de registradores y registros | — | Comisión | Registradores de partes usuarias y sus registros | 2024/2980 art. 5.1 | Cualquiera: consultar quién está registrado y para qué |
| Lista de carteras certificadas | — | Comisión | Soluciones de cartera certificadas | eIDAS art. 5d; 2025/849 | Usuarios y supervisores |

La Comisión publica las ubicaciones de las LoTE en el Diario Oficial (ARF 3.5).

## 2. Lo que dice el ARF sobre su uso

- **Para entrar en una LoTE hay que ser notificado** por un Estado. Salvo los
  proveedores de cartera, la notificación llega después de que un registrador
  haya registrado a la entidad (ARF 3.5).
- **EAA no cualificadas**: no hay lista de la Comisión. El rulebook del tipo de
  atestación dice cómo obtener el ancla, que puede ser una LoTE propia
  (ARF 6.3.2.4).
- **Partes usuarias**: no hay lista, porque serían demasiadas. La cartera las
  autentica por su certificado de acceso, que encadena hasta la LoTE de
  Access CA (ARF 3.5).
- **Pérdida de confianza**: según el ARF, una entidad **nunca se quita** de una
  Trusted List o LoTE; se cambia su estado a **Invalid** (ARF 3.5, 6.2.3 y
  6.3.3). Una cartera de un proveedor invalidado deja de recibir PID y
  atestaciones, y el proveedor revoca sus unidades.

## 3. Discrepancia pendiente (procedencia: criterio)

Hay quien afirma que en la LoTE de proveedores de PID **no hay
estado de servicio** y que al proveedor se le **quita** de la lista (citan
ETSI TS 119 602, tabla D.3). El ARF v3.0.0 dice lo contrario: nunca se quita,
se marca como Invalid. No se ha podido comprobar el texto de ETSI.

Mientras no se resuelva, el criterio prudente para quien valida es tratar como
no confiable **las dos cosas**: una entidad que ya no aparece en la lista y una
que aparece con estado distinto de válido.
