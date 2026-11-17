---
id: AV-003
titulo: "La Trusted List de verificación de edad y cómo validarla"
procedencia: mixta          # norma (§1) · observacion (§2) · criterio (§3)
fuente: "Spec. principal AV §3.4.4 y §4.5 (commit 8b97287); ETSI TS 119 612"
version_fuente: "commit 8b97287; ETSI TS 119 612 V2.4.1 (la que cita la especificación)"
url: https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/blob/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/architecture-and-technical-specifications.md
requisitos: ["Spec. principal AV §3.4.4", "§4.4", "§4.5"]
estado: borrador
verificado: 2026-11-17
revisar_antes: 2027-03-01
tags: [verificacion-de-edad, trusted-list, xades, confianza]
relacionadas: [AV-001, AV-002, CNF-001, CRI-001, CRI-002, CRI-003]
---

# La Trusted List de verificación de edad

## En una frase

Una única lista europea, en formato ETSI TS 119 612 y firmada con XAdES, que
publica la Comisión en el eIDAS Dashboard y que contiene los Attestation
Providers autorizados con su ancla de confianza.

## 1. Lo que fija la especificación (procedencia: norma)

- Base jurídica: listas operadas conforme al art. 22 de eIDAS; formato ETSI
  TS 119 612 (la especificación cita la V2.4.1).
- Publicación: eIDAS Dashboard,
  <https://eidas.ec.europa.eu/efda/trust-services/browse/av-tl>.
- Cada AP figura con su información y su **ancla de confianza** (*Service
  Digital Identifier*), que la RP usa para validar la atestación. Una RP puede
  confiar en todos los AP de la lista.
- Las altas las tramitan representantes autorizados de los Estados miembros.
- La RP *SHALL* comprobar contra esta lista que el AP está autorizado (§4.4).

**No hay lista de listas (LOTL) para AV.** Fijar el firmante de esta lista ya
ancla en la raíz: no hay un nivel superior al que encadenar.

## 2. Lo observado en la práctica (procedencia: observacion)

Medido en julio de 2026; puede cambiar.

- Hay **dos listas**: aceptación (pruebas) y producción. Están firmadas por
  certificados de **CA distintas**, así que un único certificado fijado falla en
  el entorno que no le corresponde: cada URL necesita su propio firmante fijado.
- Los AP aparecen como servicios con un tipo de servicio propio de AV y estado
  *recognized*. Si la biblioteca de validación espera tipos de servicio
  estándar, hay que mapearlo.
- En julio de 2026, la lista de producción tenía **una sola entrada** (el
  servicio danés) y la de aceptación, siete, de varios Estados.

## 3. Cómo validarla (procedencia: criterio)

Pasos que aplicamos; cada decisión discutible tiene su criterio.

1. **Descargar** la lista de la URL configurada.
2. **Verificar la firma XAdES** contra el firmante fijado para esa URL. Si no
   coincide, la lista no vale ([CRI-002](../criterios/fijar-firmante-de-la-lista.md)).
3. **Comprobar `NextUpdate`.** Una lista caducada se rechaza
   ([CRI-001](../criterios/lista-caducada.md)).
4. **Filtrar** servicios en estado *recognized* y con certificado.
5. **Encadenar** el certificado firmante del documento (el del AP) hasta un
   ancla de la lista; sin coincidencia, se rechaza.

Y dos reglas de operación:

- **Sin lista configurada no hay validación**: tratarlo como error, no como
  «nada que comprobar» ([CRI-003](../criterios/sin-lista-no-se-valida.md)).
- **Copia local de respaldo**: sirve si falla la descarga, pero debe pasar las
  mismas comprobaciones (firma y `NextUpdate`). Distinguir en los registros
  **fallo de descarga** (ruido operativo) de **fallo de verificación** (firma
  inválida o firmante distinto: evento de seguridad; desde ese momento las
  anclas son antiguas).

**Para probarlo:** la firma XAdES cubre `NextUpdate`. Para simular una lista
caducada hay que mover el reloj, no editar el XML: un documento retocado falla
antes en la firma y la prueba no demuestra lo que dice.
