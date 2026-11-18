# Glosario

Términos tal como los usan las normas. Si el uso habitual difiere, se dice.

| Término | Significado | Fuente | Confusión habitual |
|---|---|---|---|
| WUA (Wallet Unit Attestation) | Declaración de la unidad de cartera: una o varias WIA y una o varias KA | 2026/1731, anexo III | Usarlo como sinónimo de WIA |
| WIA (Wallet Instance Attestation) | Atestación de la instancia de cartera, para autenticarse ante el emisor | ARF | |
| KA (Key Attestation) | Atestación de las claves del titular y del WSCD que las guarda | ARF | |
| WSCD | Dispositivo seguro de creación de firma/sello de la cartera | ARF | |
| WRPAC | Certificado de acceso de la parte usuaria de la cartera (X.509) | ETSI TS 119 411-8 | Llamarlo «RPAC» |
| WRPRC | Certificado de registro de la parte usuaria: un JWT firmado, no un X.509 (ARF 3.19); TS 119 475 admitiría también CWT (sin verificar) | ETSI TS 119 475; ARF v3.0.0 | Llamarlo «RPRC»; creer que es X.509 |
| Access CA | Término del ARF para el proveedor de certificados de acceso | ARF | Los reglamentos usan otro nombre |
| PID | Datos de identificación personal | eIDAS art. 3 | |
| EAA / QEAA / PuB-EAA | Declaración electrónica de atributos: no cualificada / cualificada / expedida por un organismo público | eIDAS art. 3 | |
| Trusted List | Lista de confianza nacional de prestadores (XML) | ETSI TS 119 612 | |
| LoTE | Lista de entidades de confianza, para los actores de la cartera | ETSI TS 119 602 | Confundirla con la Trusted List |
| DCQL | Lenguaje de consulta de credenciales de OpenID4VP | OpenID4VP 1.0 | |
| AP / AVI | Attestation Provider / Age Verification App Instance: emisor y app del Blueprint de verificación de edad | Spec. AV §1.3 | |
| AVSUA | AVS Unit Attestation: la WUA aplicada a la app de AV (AVIA + KA) | Spec. AV, anexo A §A.5 | |
| Over-asking | Que una parte usuaria pida más atributos de los registrados | ARF; WRPRC | |

Todas las filas están pendientes de verificar contra la fuente citada.
