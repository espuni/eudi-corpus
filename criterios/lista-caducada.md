---
id: CRI-001
titulo: "Una lista de confianza caducada se rechaza"
procedencia: criterio
fuentes: ["ETSI TS 119 612 (NextUpdate)", "Spec. principal AV §3.4.4"]
confianza: alta
estado: vigente
fecha: 2026-11-17
revisar_antes:
---

# Una lista de confianza caducada se rechaza

## Ambigüedad

ETSI TS 119 612 define `NextUpdate` como la fecha en que se publicará la
siguiente versión, pero la especificación de AV no dice qué hace la RP si la
lista que tiene ya pasó esa fecha (por ejemplo, porque la descarga falla y solo
queda una copia antigua).

## Criterio

Pasada `NextUpdate`, la lista no se usa: si no hay otra copia vigente, la
validación del emisor **falla** (rechazar, no aceptar).

## Motivo

Una lista caducada puede seguir conteniendo emisores ya retirados. Aceptar con
ella convierte un fallo de disponibilidad en un fallo de seguridad silencioso.
Conviene además avisar con antelación (por ejemplo, tres semanas) de que se
acerca la fecha, para que no se descubra el día en que deja de validar.

## Qué lo cambiaría

Una indicación explícita de la Comisión o de ETSI sobre un periodo de gracia.
