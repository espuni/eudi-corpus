# Preguntas de evaluación

Para comprobar si un asistente de IA responde bien con este corpus. Cada
pregunta tiene una respuesta cerrada y la cita que la sostiene. Se pasa la
batería completa cada vez que cambia el corpus o el asistente, y se anota el
resultado al final.

Solo entran preguntas cuya respuesta esté **verificada** contra la fuente.

| ID | Pregunta | Respuesta de referencia | Cita | Trampa habitual |
|---|---|---|---|---|
| EVA-001 | ¿Tiene que ser un QTSP el proveedor de certificados de acceso de partes usuarias? | No lo exige el acto: es una autoridad de certificación que el Estado autoriza | 2025/848 art. 7.1; ARF 3.5 | Suponer que todo lo que firma certificados en eIDAS es cualificado |
| EVA-002 | ¿Una PuB-EAA va firmada con un certificado cualificado? | Sí: firma o sello cualificado del organismo, con un certificado que identifica la ley que lo habilita y la fuente auténtica | eIDAS art. 45f.1.b y anexo VII, g | Confundirla con una EAA no cualificada porque el organismo no es QTSP |
| EVA-003 | ¿Qué incluye una WUA? | Una o varias WIA y una o varias KA | 2026/1731, anexo III | Usar WUA y WIA como sinónimos |
| EVA-004 | ¿Desde cuándo tiene que validar la cartera el certificado de registro de la parte usuaria? | Desde el 11-8-2028 | 2024/2982 art. 3.4 y art. 8 (redacción de 2026/1731) | Dar por hecho que es exigible ya |
| EVA-005 | ¿Están obligados los Estados a autorizar proveedores de certificados de registro? | Sí, al menos uno, desde 2026/1730 (antes era opcional) | 2025/848 art. 8.1, modificado por 2026/1730 | Citar la redacción original («may authorise») |
| EVA-006 | En la suspensión de una solución de cartera, ¿hay que revocar las WUA? | No necesariamente: se evalúa. En la retirada, sí, de forma irreversible | 2025/847 arts. 4.2 y 8.2 | Tratar suspensión y retirada como lo mismo |
| EVA-007 | Si se revoca la WUA de una unidad, ¿qué pasa con el PID que tiene? | El proveedor de PID tiene que revocarlo, de forma irreversible | 2024/2977 art. 5.4.b y 5.5 | Creer que la regla vale igual para cualquier EAA |
| EVA-008 | ¿Dónde se ancla la confianza en un proveedor de QEAA y en uno de PID? | QEAA: Trusted List nacional (TS 119 612). PID: LoTE de la Comisión (TS 119 602) | ARF 3.5; eIDAS art. 22 | Buscar las QEAA en una LoTE |
| EVA-009 | ¿Recibe un proveedor de cartera certificado de acceso o de registro? | No: no se registra; se notifica y sus anclas van a la LoTE de proveedores de cartera | ARF 6.2.2 | Tratarlo como una parte usuaria más |
| EVA-011 | ¿Qué política mínima aplica el proveedor de certificados de acceso? | La NCP de ETSI EN 319 411-1; las políticas cualificadas son opcionales | TS 119 411-8, OVR-4.2.2-02 | Suponer que tiene que ser QCP |
| EVA-012 | Si un proveedor de PID deja de ser de confianza, ¿cómo se refleja en su LoTE? | Se quita de la lista: esa LoTE no tiene estado de servicio (el ARF dice que se marca Invalid; manda el formato de ETSI) | TS 119 602, tabla D.3 | Buscar un estado «Invalid» que no existe en ese perfil |
| EVA-013 | ¿Tiene que admitir un proveedor de PID los dos flujos de OpenID4VCI? | No: al menos uno. La cartera, los dos | TS 119 472-3 GEN-REQ-4.1-03 y -04 | Exigir los dos al emisor |
| EVA-014 | ¿Exige la norma presencia física para emitir PID con *pre-authorised code*? | No: 2026/1731 deja sin efecto GEN-REQ-4.1-05 | 2026/1731 anexo XI | Citar la TS sin sus adaptaciones |
| EVA-015 | ¿En qué peticiones va la WIA y en cuál la KA? | WIA: PAR y token. KA: petición de credencial, en `proofs` | 2026/1731 anexo III, TR-WIA-3 y TR_KA-3 | Mandar la KA al token |
| EVA-016 | ¿Qué tipos de prueba tiene que admitir un emisor de credenciales ligadas al dispositivo? | `jwt` y `attestation`, los dos | 2026/1731 anexo III, TR_KA-4 | Admitir solo `jwt` |
| EVA-017 | ¿Cómo indica una SD-JWT VC que es una QEAA? | Con la claim `category` | TS 119 472-1 QEAA-5.2.2.2-01 | Buscarlo solo en el certificado |
| EVA-018 | ¿Tiene que comprobar la parte usuaria la lista de revocación de un mdoc? | Es opcional; si la comprueba, admite los dos mecanismos (lista de estado y de identificadores) | 2026/1731 anexo IV, EAA-6.2.10.1-05 y -05.1 | Darlo por obligatorio |
| EVA-019 | ¿Cómo recibe la cartera el certificado de registro en una petición mdoc? | En `requestInfo`, miembro `euWrprc`, codificado en CBOR | 2026/1731 anexo XII, ISO/IEC 18013-5-REQ-04 a -07 | Creer que solo existe en OpenID4VP |
| EVA-020 | ¿Es obligatoria la Digital Credentials API para la parte usuaria? | Sí: 2026/1731 la hace obligatoria para cartera y parte usuaria (OIDFVP-HAIP-SUPPORT-05) | 2026/1731 anexo XII | Citar la TS, donde era opcional |
| EVA-010 | ¿Qué plazo hay para retirar una solución suspendida cuya brecha no se ha remediado? | Tres meses desde la suspensión; la retirada, en 72 h tras ese plazo | 2025/847 art. 8.1 | Confundir las 72 h con las 24 h de aviso |

## Resultados

| Fecha | Asistente / modelo | Corpus (commit) | Aciertos | Notas |
|---|---|---|---|---|
