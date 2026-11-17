---
id: OBS-001
titulo: "Una prueba ZK de ~360 KB no vuelve por el flujo cross-device de la Digital Credentials API"
procedencia: observacion
fuente: "Medición propia; contexto en EU AV Blueprint anexo A §A.8 y Digital Credentials API (W3C)"
version_fuente: "Chrome 151 escritorio; app de referencia AV para Android; circuito longfellow v7"
url: ""
requisitos: ["AV anexo A §A.8"]
estado: borrador
verificado: 2026-08-30
revisar_antes: 2027-03-01
tags: [dc-api, cross-device, zk, longfellow, verificacion-de-edad, ctap-hybrid]
relacionadas: [PRO-005, AV-004, PRO-010]
---

# Una prueba ZK grande no vuelve por el flujo cross-device de la DC API

## En una frase

La presentación ZK del perfil de AV funciona en el mismo dispositivo y falla en
cross-device (navegador de escritorio + QR + móvil) **después** de que el usuario
apruebe; la única variable es el tamaño de la respuesta.

## Resultado

| | Divulgación selectiva (ISO 18013-5) | ZK (longfellow v7) |
|---|---|---|
| Tamaño de la respuesta | unos KB | ~360 KB (~480 KB en base64url) |
| Mismo dispositivo (Chrome Android) | funciona | funciona |
| Cross-device (escritorio + QR) | funciona | **falla** |

En cross-device, el diálogo del sistema muestra el wallet y la credencial
pedida, el usuario aprueba y Chrome devuelve su error genérico
(`Error retrieving a token.`). La respuesta nunca llega al verifier.

## Método

Todo fijo salvo el tipo de prueba: misma página, mismo `DeviceRequest` CBOR
byte a byte, mismo protocolo (`org-iso-mdoc`), mismo wallet con credencial de
pruebas, mismo verifier.

Descartado:

- **Configuración del verifier:** fallaría antes de abrir el wallet.
- **El wallet no soporta cross-device:** el diálogo aparece con la credencial y
  acepta la aprobación.
- **Petición distinta en cada flujo:** es la misma.
- **Límite de tamaño del cuerpo en el servidor:** la petición ni siquiera llega.
- **El navegador no soporta cross-device:** funciona con la respuesta pequeña.

## Causa probable

El transporte cross-device de la DC API es **CTAP 2.2 hybrid** (QR + BLE de
proximidad + servidor de túnel), el mismo de las passkeys, dimensionado para
aserciones FIDO del orden de 1 KB. No se ha encontrado un límite de tamaño
documentado ni en la especificación del W3C ni en la documentación de Chrome.

Hipótesis no descartada: **timeout** del túnel mientras el móvil genera la
prueba. Se distinguiría midiendo el tiempo entre la aprobación y el error.

## Consecuencias

- Hoy la verificación ZK es solo **mismo dispositivo**. No hay fallback por QR:
  el QR clásico devuelve un `vp_token` normal, no una prueba ZK.
- En escritorio, la alternativa es OpenID4VP con QR y divulgación selectiva,
  que no es ZK.
- El fallo llega en el peor momento, después del consentimiento, y es
  indistinguible de «sin credencial» o «cancelado».

## Preguntas abiertas

- ¿Límite duro o timeout? ¿A partir de qué tamaño falla?
- ¿Se comporta igual con wallets de otros fabricantes?

## Cómo reproducirlo

1. Portátil con Chrome ≥ 141 y móvil Android con el wallet de referencia de AV y
   una credencial sin usar (son de un solo uso).
2. Verifier con DC API `org-iso-mdoc`. Presentación selectiva en cross-device:
   debe funcionar.
3. Repetir con prueba ZK: falla tras aprobar.
4. Repetir la prueba ZK abriendo la página en el móvil: funciona.
