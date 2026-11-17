---
id: CRI-002
titulo: "Se fija el certificado exacto que firma la lista, no su CA"
procedencia: criterio
fuentes: ["ETSI TS 119 612 (firma XAdES de la lista)", "Spec. principal AV §3.4.4"]
confianza: media
estado: vigente
fecha: 2026-11-17
revisar_antes:
---

# Se fija el certificado exacto que firma la lista

## Ambigüedad

La especificación dice dónde se publica la lista, pero no cómo debe la RP
autenticar quién la firmó: fijar el certificado del firmante, encadenarlo hasta
su CA o fiarse del canal HTTPS.

## Criterio

Se fija el **certificado exacto** del firmante, uno por cada lista (aceptación
y producción), y se configura de forma que pueda cambiarse sin desplegar código.

## Motivo

Comprobar quién firmó la lista es lo que la convierte en evidencia y no en una
descarga. Fijar el certificado es lo más estricto. El coste es operativo: una
rotación del firmante rompe la validación hasta que se actualiza el valor
fijado, por eso tiene que poder cambiarse por configuración y el fallo de firma
tiene que alertar.

## Qué lo cambiaría

Que la Comisión publique el certificado y su calendario de rotación por un
canal autenticado, o que exista una LOTL para AV; entonces encadenar a la CA
sería suficiente.
