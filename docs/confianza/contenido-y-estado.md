---
id: CNF-006
titulo: "Contenido y estado de PID, QEAA y PuB-EAA: TS 119 472-1 y el anexo IV de 2026/1731"
procedencia: mixta          # norma (§1-§4) · criterio (§5)
fuente: "ETSI TS 119 472-1 V1.2.1 (2026-02), aplicada por CIR 2024/2979 anexo II en la redacción de 2026/1731 (anexo IV)"
version_fuente: "TS 119 472-1 V1.2.1 (2026-02); textos oficiales vía inventario 300f644"
url: https://www.etsi.org/deliver/etsi_ts/119400_119499/11947201/01.02.01_60/ts_11947201v010201p.pdf
requisitos: ["QEAA-5.2.2.2-01", "PuB-EAA-5.2.2.3-01", "EAA-5.2.2.1-01", "PuB-EAA-4.2.6.8-01", "QEAA-5.6.2-02", "PuB-EAA-5.6.3-02", "QEAA-6.6.2-02", "EAA-4.2.11.1-06", "EAA-6.2.10.1-01 a -07"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [eaa, qeaa, pub-eaa, pid, sd-jwt-vc, mdoc, estado, revocacion, token-status-list]
relacionadas: [ARF-001, CNF-008, CNF-007, ARF-003]
---

# Contenido y estado de PID, QEAA y PuB-EAA

## En una frase

La propia credencial dice si es QEAA o PuB-EAA (`category` en SD-JWT VC), lleva
en la firma dónde está el certificado (`x5u` y su huella), y su estado solo
admite «revocado», de forma permanente.

## 1. Qué obliga

2024/2979, anexo II (redacción de 2026/1731, anexo IV): se aplican las
cláusulas 2 a 6 de **ETSI TS 119 472-1 V1.2.1 (2026-02)**, con adaptaciones en
el estado (4.2.11.1 y 6.2.10.1), entre otras.

## 2. Marcar el tipo en la credencial

| | SD-JWT VC | mdoc |
|---|---|---|
| QEAA | Lleva la claim **`category`**, con un URN definido en la TS (QEAA-5.2.2.2-01 y -02) | — |
| PuB-EAA | Lleva la claim **`category`** (PuB-EAA-5.2.2.3-01) | — |
| EAA no cualificada | **No** lleva `category` (EAA-5.2.2.1-01) | — |
| Firma de QEAA | Cabecera protegida con **`x5u`** y **`x5t#S256`** (QEAA-5.6.2-02) | CB-AdES con `x5u` y `x5t` (RFC 9360) (QEAA-6.6.2-02) |
| Firma de PuB-EAA | `x5u` y `x5t#S256` (PuB-EAA-5.6.3-02) | CB-AdES con `x5u` y `x5t` (PuB-EAA-6.6.3-02) |

Una PuB-EAA incluye el identificador de su sujeto o un seudónimo
(PuB-EAA-4.2.6.8-01). La base está en eIDAS, anexos V y VII: la indicación de
tipo (letra a), el sujeto (letra c) y dónde obtener el certificado (letra h).

## 3. Estado

Adaptaciones de 2026/1731 sobre TS 119 472-1:

- En PID, QEAA y PuB-EAA, el estado **solo** indica si la atestación está
  revocada (EAA-4.2.11.1-06), y una revocación es **permanente**
  (EAA-4.2.11.1-06.1). En una Token Status List eso significa usar solo los
  valores `valid` e `invalid` (EAA-6.2.10.1-03.1).
- En mdoc, el emisor usa una **lista de estado** (Token Status List,
  `draft-ietf-oauth-status-list-20`) o una **lista de identificadores
  revocados** (EAA-6.2.10.1-02). La lista va como *status list token* en
  formato **CWT** (EAA-6.2.10.1-07).
- Las atestaciones de **24 h o menos** no necesitan revocación
  (EAA-6.2.10.1-02.1).
- Para la parte usuaria, **comprobar la lista de revocación de un mdoc es
  opcional**. Si la comprueba, sigue la especificación de Token Status List, y
  tiene que admitir **los dos** mecanismos (EAA-6.2.10.1-05 y -05.1).
- Ancla del firmante de la lista: si la lista lleva el elemento `certificate`,
  ese certificado es el ancla. Si no, el primer certificado de su `x5chain`
  tiene que estar firmado por el mismo certificado que firmó el del `x5chain`
  del MSO (EAA-6.2.10.1-06.1 y -06.2).

## 4. Relación con la cartera

- Si se revoca la WUA, el **PID** se revoca obligatoriamente (2024/2977
  art. 5.4.b). Para las EAA no es obligatorio (ARF 6.6.2.5).
- Las atestaciones emitidas a la cartera cumplen al menos uno de los formatos
  del anexo II de 2024/2979 (2024/2977 art. 4.1, redacción de 2026/1731).

## 5. Lo que conviene tener claro (procedencia: criterio)

- **«Opcional para la parte usuaria» no significa irrelevante.** Que el acto
  no obligue a comprobar el estado de un mdoc no quita que, si se comprueba, se
  haga entero: los dos mecanismos y el ancla correcta del firmante de la
  lista. Un verificador que solo admite uno de los dos falla con los emisores
  que usen el otro.
- **Un verificador que valida QEAA o PuB-EAA** debe comprobar la marca de tipo
  (`category`) además de la firma. Si no, una EAA no cualificada firmada por un
  QTSP pasaría por cualificada.
