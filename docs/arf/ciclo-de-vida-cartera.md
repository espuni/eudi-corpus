---
id: ARF-003
titulo: "Ciclo de vida: suspensión y retirada de la cartera, revocación de WUA y PID, y pérdida de confianza en un proveedor"
procedencia: mixta          # norma (§1-§4) · criterio (§5)
fuente: "CIR 2025/847; CIR 2024/2979 art. 7; CIR 2024/2977 art. 5 (redacción de 2026/1731); ARF v3.0.0 6.2.3, 6.3.3, 6.5.4.2, 6.6.2.5"
version_fuente: "textos oficiales vía inventario 300f644; ARF v3.0.0"
url: https://data.europa.eu/eli/reg_impl/2025/847/oj/eng
requisitos: ["2025/847 arts. 3 a 10", "2024/2979 art. 7", "2024/2977 art. 5", "2026/1731 anexo III", "ARF 6.5.4.2", "ARF 6.6.2.5"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [ciclo-de-vida, suspension, retirada, revocacion, wua, pid, ciras]
relacionadas: [ARF-001, CNF-009, LEG-016]
---

# Ciclo de vida: suspensión, retirada y revocación

## En una frase

Lo que se suspende o retira es la **solución de cartera**, y lo decide el
Estado; lo que se revoca son las **atestaciones de las unidades** (WUA), y
revocar la WUA obliga al proveedor de PID a revocar el PID.

## 1. Vocabulario

- **WUA** (declaración de unidad de cartera): comprende **una o varias WIA y una
  o varias KA** (2026/1731, anexo III). No es sinónimo de WIA.
- **Solución de cartera** frente a **unidad de cartera**: la solución es el
  producto certificado; la unidad, la configuración concreta que usa cada
  usuario (2025/847 art. 2).

## 2. Suspensión y retirada de la solución (2025/847)

| | Suspensión | Retirada |
|---|---|---|
| Quién decide | El Estado, tras evaluar la brecha con los criterios del anexo I (art. 3) | El Estado |
| Cuándo | Brecha o compromiso que afecta a la fiabilidad | Si la brecha **no se remedia en tres meses** desde la suspensión, o directamente por su gravedad (art. 8.1 y 9.2.f) |
| Qué se hace | No se proporcionan, usan ni activan unidades (art. 4.1). **Se evalúa** si revocar las WUA (art. 4.2) | Se **revocan** las WUA, sin vuelta atrás; no se emiten WUA nuevas a unidades existentes ni unidades nuevas (art. 8.2) |
| Plazo | Medidas en **24 h** desde la suspensión (art. 4.3) | Retirada en **72 h** tras cumplirse los tres meses (art. 8.1) |
| A quién se informa, en 24 h | Puntos de contacto únicos, Comisión, usuarios afectados y partes usuarias registradas (art. 5.1) | Los mismos (art. 9.1) |
| Por dónde | A la Comisión y a los puntos de contacto, por **CIRAS** (ENISA) o equivalente (art. 10, aplicable **desde el 7 de mayo de 2026**) | Igual |
| Portabilidad | Las medidas no impiden al usuario ejercer la portabilidad de sus datos si es seguro (art. 4.4) | Igual (art. 8.3) |

**Restablecimiento** (art. 6): nueva versión de la solución para los usuarios
afectados, o nuevas WUA a las unidades que cumplan los requisitos tras la
corrección, y levantar las medidas ligadas solo a esa brecha. Se informa a los
mismos destinatarios (art. 7).

No existe un estado «suspendido» de la **unidad** ni de sus atestaciones: la
suspensión es de la solución.

## 3. Revocación de WUA y de PID

| | WUA | PID |
|---|---|---|
| Quién puede revocar | Solo el proveedor de cartera (2024/2979 art. 7.1) | Solo su proveedor (2024/2977 art. 5.2) |
| Cuándo | Según su política pública (art. 7.2); el ARF lista pérdida o robo, fallecimiento comunicado por el proveedor de PID, brecha en la unidad, suspensión (opcional) o retirada (obligatoria) de la solución, e invalidación del proveedor (ARF 6.5.4.2) | A petición del usuario; **si se ha revocado la WUA de la unidad**; o según su política (art. 5.4) |
| Aviso al usuario | En **24 h**, con motivo y consecuencias (art. 7.3) | En **24 h**, con motivo (art. 5.3) |
| Reversible | — | **No** (art. 5.5) |
| Publicación del estado | Pública y que preserve la privacidad (art. 7.4) | Igual (art. 5.7) |

Hay, por tanto, **cuatro plazos de 24 h distintos**: las medidas de suspensión,
los dos avisos de suspensión o retirada, el aviso de revocación de WUA y el de
revocación de PID.

**EAA**: el reglamento no obliga a revocar una EAA cuando se revoca la WUA.
Los proveedores de atestaciones pueden usar el mismo mecanismo que los de PID
(ARF 6.6.2.5).

## 4. Pérdida de confianza en un proveedor (ARF)

- **Proveedor de cartera invalidado**: el Estado pide cambiar su estado en la
  LoTE a Invalid; los emisores dejan de confiar en sus WIA y KA, y el
  proveedor revoca sus unidades (ARF 6.2.3).
- **Proveedor de PID o de atestaciones con el registro suspendido o
  cancelado**: se revocan sus certificados de acceso, su estado pasa a Invalid
  en la lista que le corresponda, y revoca lo que emitió (ARF 6.3.3).

## 5. Lo que se suele confundir (procedencia: criterio)

- «Cancelar el rol del proveedor de cartera» no es lo que regula 2025/847: ese
  acto trata de la **solución**. La invalidación del proveedor en la LoTE la
  describe el ARF, no el acto.
- La suspensión **no obliga** a revocar las WUA; la retirada sí. Un sistema que
  revoque siempre en la suspensión es más estricto que la norma, pero cuidado:
  la revocación es irreversible y obliga a reemitir WUA al restablecer.
