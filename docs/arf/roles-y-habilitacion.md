---
id: ARF-001
titulo: "Roles del ecosistema: quién los habilita, qué certificados reciben y cuáles son QTSP"
procedencia: mixta          # norma (§1-§3) · criterio (§4)
fuente: "eIDAS consolidado (2024-10-18); CIR 2025/848 modificado por 2026/1730; CIR 2024/2980 modificado por 2026/1731; ARF v3.0.0 cap. 3 y 6"
version_fuente: "textos oficiales vía inventario 300f644; ARF v3.0.0"
url: https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v3.0.0/docs/main/03-roles-within-the-eudi-wallet-ecosystem.md
requisitos: ["eIDAS art. 3(45) y 3(46)", "eIDAS art. 45d y 45f", "2025/848 art. 7.1 y 8.1", "2024/2980 art. 5", "ARF 3.5, 3.18, 3.19, 6.2.2, 6.3.2.3, 6.3.2.4"]
estado: borrador
verificado: 2026-11-18
revisar_antes: 2027-05-01
tags: [roles, qtsp, qeaa, pub-eaa, wrpac, wrprc, registro, confianza]
relacionadas: [CNF-003, CNF-009, ARF-003, LEG-017, LEG-019]
---

# Roles del ecosistema y quién los habilita

## En una frase

Solo el proveedor de QEAA es por definición un prestador cualificado (QTSP).
El resto de roles los habilita el Estado miembro por otras vías: registro,
autorización o notificación a la Comisión, que los publica en una LoTE.

## 1. Tabla de roles

| Rol | Quién lo habilita | ¿Registrado (2025/848)? | ¿Certificado de acceso y de registro? | Dónde están sus anclas | ¿QTSP? |
|---|---|---|---|---|---|
| Proveedor de cartera | El Estado lo notifica tras certificar la solución (2024/2980) | **No** | **No**: solo se comunica con sus propias unidades (ARF 6.2.2) | LoTE de proveedores de cartera | No |
| Proveedor de PID | Registro + notificación del Estado | Sí | Sí, ambos (ARF 6.3.2.3) | LoTE de proveedores de PID | No es requisito |
| Proveedor de QEAA | Estatus cualificado (supervisión, Trusted List) + registro | Sí | Sí, ambos | **Trusted List** nacional (TS 119 612) | **Sí**: la QEAA la expide un QTSP (eIDAS art. 3(45)) |
| Organismo que expide PuB-EAA | El Estado lo notifica con informe de un CAB (eIDAS art. 45f.3) | Sí | Sí, ambos | LoTE de organismos PuB-EAA | No, pero con fiabilidad **equivalente** a un QTSP (art. 45f.2) |
| Proveedor de EAA no cualificada | Registro | Sí | Sí, ambos | Ninguna lista de la Comisión; el rulebook del tipo dice cómo obtener el ancla (ARF 6.3.2.4) | No |
| Parte usuaria | Registro en su Estado | Sí | Sí: un certificado de acceso por instancia (ARF 3.18) | **Ninguna lista**: la cartera la autentica por su certificado de acceso | No |
| Proveedor de certificados de acceso (Access CA) | El Estado lo **autoriza** (al menos uno, 2025/848 art. 7.1) y lo notifica | — | — | LoTE de Access CA | No es requisito del acto |
| Proveedor de certificados de registro | El Estado lo **autoriza**: obligatorio desde 2026/1730 («shall authorise», antes «may») | — | — | LoTE de proveedores de certificados de registro (2024/2980 art. 5.2, desde 2026/1731) | No es requisito del acto |

Sobre la última columna, el ARF dice expresamente que los proveedores de
cartera, de PID, de PuB-EAA, las Access CA y los proveedores de certificados de
registro **no son prestadores de servicios de confianza** en el sentido de
eIDAS. Por eso van en una LoTE y no en una Trusted List (ARF 3.5).

## 2. QEAA frente a PuB-EAA frente a EAA

| | QEAA | PuB-EAA | EAA no cualificada |
|---|---|---|---|
| Definición | eIDAS art. 3(45) | eIDAS art. 3(46) | eIDAS art. 3(44) |
| Quién la expide | Un QTSP | Un organismo público responsable de una fuente auténtica, o designado para actuar en su nombre | Cualquier prestador |
| Firma | Firma o sello **cualificado** del QTSP (anexo V, letra g) | Firma o sello **cualificado** del organismo (anexo VII, letra g; art. 45f.1.b) | No exigida por eIDAS |
| Certificado | Cualificado | Cualificado, con atributos que identifican la ley que habilita al organismo y la fuente auténtica (art. 45f.1.b, i a iii) | — |
| Marca en la propia credencial | Indicación legible por máquina de que es QEAA (anexo V, a) | Indicación de que es PuB-EAA (anexo VII, a) | — |
| Revocación | Irreversible (art. 45d.4) | Irreversible (art. 45f.4) | Según el emisor |

En la versión española de eIDAS, el art. 45d es el **45 quinquies** y el 45f
el **45 septies**.

## 3. Lo que depende de ETSI y no se ha verificado aquí

Estos puntos se citan a menudo y son plausibles, pero no se han
podido comprobar contra el texto de ETSI. ETSI no permite la descarga
automatizada desde el entorno donde se escribió esta ficha:

- el proveedor de certificados de acceso aplica como mínimo la política NCP, y
  las políticas cualificadas son opcionales (TS 119 411-8);
- el proveedor de certificados de registro puede figurar como cualificado o no
  (TS 119 475);
- el certificado del proveedor de PID lleva el QcType `id-etsi-qct-pid`, y el
  del organismo PuB-EAA, el `QcPSB` (TS 119 412-6).

## 4. Nivel de garantía (procedencia: criterio)

Preguntar «qué LoA tiene cada rol» lleva a error. Los actos exigen el nivel
**alto** a operaciones concretas de la cartera: las de su dispositivo seguro
(WSCD) cuando sirven para identificación electrónica de nivel alto
(2024/2979 arts. 4.3 y 5.1), y al PID. No hay un nivel de garantía atribuido a
cada rol.
