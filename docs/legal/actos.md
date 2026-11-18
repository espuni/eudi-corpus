---
id: LEG-000
titulo: Tracker de actos legales
procedencia: norma
estado: borrador
verificado:
revisar_antes:
---

# Tracker de actos legales

Tracker editable: aquí se anotan fechas de aplicación, modificaciones y la
verificación. La lista completa de actos, con CELEX, ELI y las normas que cita
cada uno, se genera desde el inventario de Giuseppe De Marco en
[Legislación de la UE](../referencias/legislacion.md).

**Nada de esta tabla está verificado todavía.** Hay que confirmar cada fila en
EUR-Lex (columna *Verificado*), en especial las fechas de aplicación.

Enlaces ELI: reglamento `https://eur-lex.europa.eu/eli/reg/AAAA/NNNN/oj`,
reglamento de ejecución `https://eur-lex.europa.eu/eli/reg_impl/AAAA/NNNN/oj`.

## Marco

| ID | Acto | Objeto | Capa | Aplica desde | Modificado por | Verificado |
|---|---|---|---|---|---|---|
| LEG-001 | Reglamento (UE) 910/2014 (eIDAS) | Identificación electrónica y servicios de confianza | Todo | | 2024/1183 | — |
| LEG-002 | Reglamento (UE) 2024/1183 (eIDAS 2) | Marco europeo de identidad digital; introduce la cartera | Todo | | | — |

## Actos de ejecución de la cartera

| ID | Acto | Objeto | Capa | Aplica desde | Modificado por | Verificado |
|---|---|---|---|---|---|---|
| LEG-010 | Reglamento de Ejecución (UE) 2024/2977 | PID y declaraciones electrónicas de atributos | Emisión | | 2026/1731 | — |
| LEG-011 | Reglamento de Ejecución (UE) 2024/2979 | Integridad y funcionalidades básicas de la cartera | Cartera | | 2026/1731 | — |
| LEG-012 | Reglamento de Ejecución (UE) 2024/2980 | Marco de confianza y notificaciones a la Comisión | Confianza | | 2026/1731 | — |
| LEG-013 | Reglamento de Ejecución (UE) 2024/2981 | Certificación de las carteras | Cartera | | | — |
| LEG-014 | Reglamento de Ejecución (UE) 2024/2982 | Protocolos e interfaces | Emisión, presentación | | 2026/1731 | — |
| LEG-015 | Reglamento de Ejecución (UE) 2025/846 | Correspondencia transfronteriza de identidad | Presentación | | | — |
| LEG-016 | Reglamento de Ejecución (UE) 2025/847 | Respuesta a violaciones de seguridad de la cartera | Ciclo de vida | Art. 10 (CIRAS) desde el 7-5-2026 | | texto oficial, 2026-11-18 |
| LEG-017 | Reglamento de Ejecución (UE) 2025/848 | Registro de las partes usuarias | Confianza, presentación | 24-12-2026 | 2026/1730 | texto oficial, 2026-11-18 |
| LEG-018 | Reglamento de Ejecución (UE) 2025/849 | Información para la lista de carteras certificadas | Confianza | | | — |
| LEG-019 | Reglamento de Ejecución (UE) 2026/1730 | Modifica 2025/848 (registro de partes usuarias): los Estados **deben** autorizar al menos un proveedor de certificados de registro; cita TS 119 411-8 y TS 119 475 | Confianza, presentación | A los 20 días de su publicación en el DO (adoptado el 15-7-2026; fecha de publicación sin comprobar) | | texto oficial, 2026-11-18 |
| LEG-020 | Reglamento de Ejecución (UE) 2026/1731 | Modifica 2024/2977, 2979, 2980 y 2982: normas y especificaciones de referencia (TS 119 472-1/2/3, OpenID4VCI, OpenID4VP, HAIP, ISO/IEC 18013-5 y TS 18013-7…) | Todo | A los 20 días de su publicación en el DO (adoptado el 15-7-2026; fecha de publicación sin comprobar). El art. 3.4 de 2024/2982 que introduce, desde el 11-8-2028 | | texto oficial, 2026-11-18 |
| LEG-021 | Reglamento de Ejecución (UE) 2026/798 | Incorporación remota a la cartera (nivel sustancial) | Emisión | | | — |
| LEG-022 | Reglamento de Ejecución (UE) 2025/1569 | Verificación de atributos en declaraciones electrónicas | Confianza (QEAA) | | 2026/1735 | — |
| LEG-023 | Decisión de Ejecución (UE) 2025/2164 | Listas de confianza de prestadores de servicios de confianza (cita TS 119 612 V2.4.1) | Confianza | | | — |

El resto de actos de servicios de confianza está en
[Legislación de la UE](../referencias/legislacion.md); se traen aquí cuando una
ficha los necesite.

## Otros marcos que se cruzan

| ID | Acto | Objeto | Capa | Aplica desde | Modificado por | Verificado |
|---|---|---|---|---|---|---|
| LEG-030 | Reglamento (UE) 2022/2065 (DSA), art. 28 | Protección de menores en plataformas en línea | Verificación de edad | | | — |
| LEG-031 | Directrices de la Comisión sobre el art. 28.1 DSA | Orientación, no vinculante | Verificación de edad | | | — |
| LEG-032 | Reglamento (UE) 2016/679 (RGPD) | Protección de datos | Todo | | | — |

## Fechas que condicionan

Una línea por fecha, con el artículo que la fija.

| Fecha | Qué ocurre | Fuente | Verificado |
|---|---|---|---|
| 7-5-2026 | Las notificaciones de brechas de la cartera van por CIRAS | 2025/847 art. 11 | texto oficial, 2026-11-18 |
| 15-7-2026 | **Adopción** de 2026/1730 y 2026/1731. No es la fecha de aplicación: entran en vigor a los 20 días de su publicación | 2026/1730 y 2026/1731, fórmula final | texto oficial, 2026-11-18 |
| 24-12-2026 | Aplica el registro de partes usuarias | 2025/848 art. final | texto oficial, 2026-11-18 |
| 11-8-2028 | La cartera tiene que validar el certificado de registro de la parte usuaria | 2024/2982 art. 3.4 y art. 8, en la redacción de 2026/1731 | texto oficial, 2026-11-18 |
| 11-8-2028 | El retrato puede formar parte de los datos obligatorios del PID | 2026/1731, considerando 3 y anexo I | texto oficial, 2026-11-18 |
