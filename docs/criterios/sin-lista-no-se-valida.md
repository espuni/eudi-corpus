---
id: CRI-003
titulo: "Una verificación sin lista de confianza configurada es un error, no un aprobado"
procedencia: criterio
fuentes: ["OpenID4VP 1.0 (DCQL, trusted_authorities)", "Spec. principal AV §4.4"]
confianza: alta
estado: vigente
fecha: 2026-11-17
revisar_antes:
---

# Sin lista de confianza configurada, la verificación es un error

## Ambigüedad

DCQL permite declarar en `trusted_authorities` qué emisores acepta el
verifier, pero es opcional. Algunos verifiers interpretan su ausencia como
«no hay nada que comprobar» y dan la credencial por buena tras verificar solo la
firma.

## Criterio

Para credenciales cuyo marco exige validar al emisor (AV, PID, EAA), una
configuración sin lista de confianza **se rechaza al guardarla**, y en tiempo de
verificación se trata como fallo.

## Motivo

Una firma válida de cualquiera no prueba nada: la validación contra la lista es
lo que convierte «firmado por alguien» en «firmado por un emisor autorizado»
(Spec. AV §4.4). El fallo opuesto es silencioso y solo se descubre auditando.

Corolario: si a algún wallet hay que enviarle la consulta sin
`trusted_authorities` porque no lo tolera, se quita solo de la copia que se
envía; la configuración con la que se valida en servidor no cambia.

## Qué lo cambiaría

Nada previsible: es una propiedad de seguridad, no una interpretación de texto.
