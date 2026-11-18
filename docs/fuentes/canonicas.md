# URL canónicas

Dónde está cada familia de documentos. Siempre se cita la URL de la **versión** citada, no la de la última.
La versión exacta de cada fuente, cuándo se revisó y cuándo toca volver a mirarla están en el
[seguimiento de fuentes](index.md).

## Legal

- EUR-Lex: https://eur-lex.europa.eu/ (patrones ELI en [`legal/actos.md`](../legal/actos.md))
- Directrices art. 28 DSA: https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors

## Inventario de referencias (De Marco)

- Repositorio: https://github.com/peppelinux/eidas-references-search-engine (Apache-2.0)
- Informe: https://peppelinux.github.io/eidas-references-search-engine/report/index.html
- Uso en este corpus: los actos y las citas acto → norma del
  [catálogo de documentos referenciados](../referencias/index.md), generados con
  [`scripts/importar_inventario.py`](https://github.com/espuni/eudi-corpus/blob/main/scripts/importar_inventario.py)
  desde un commit fijado.
  Es una fuente secundaria: sirve para descubrir qué cita cada acto, no para citarlo.

## ARF y documentación de la Comisión

- ARF, versión fijada v3.0.0: https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/tree/v3.0.0
- Especificaciones técnicas TS01–TS14, sus OpenAPI y sus discusiones (fuente canónica; versiones y enlaces fijados en [`arf/especificaciones-tecnicas.md`](../arf/especificaciones-tecnicas.md)): https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/tree/main/docs/technical-specifications
- Implementación de la cartera EUDI: https://digital-strategy.ec.europa.eu/en/policies/eudi-wallet-implementation

## ETSI

- Catálogo de normas (descarga gratuita): https://www.etsi.org/standards-search

## OpenID Foundation

- OpenID4VCI 1.0: https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html
- OpenID4VP 1.0: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html
- HAIP 1.0: https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html

## IETF y W3C

- SD-JWT VC: https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/
- Token Status List: https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/
- Attestation-based client authentication: https://datatracker.ietf.org/doc/draft-ietf-oauth-attestation-based-client-auth/
- Digital Credentials API: https://github.com/w3c-fedid/digital-credentials

## Verificación de edad

- Portal técnico: https://ageverification.dev/
- Especificación técnica: https://github.com/eu-digital-identity-wallet/av-doc-technical-specification
  (sin versiones etiquetadas desde la v1.0.6 de julio de 2025; las fichas citan el commit `8b97287`, 2026-09-02)
- Trusted List de AV en el eIDAS Dashboard: https://eidas.ec.europa.eu/efda/trust-services/browse/av-tl
- Política de la Comisión: https://digital-strategy.ec.europa.eu/en/policies/eu-age-verification

## ISO

- ISO/IEC 18013-5 y TS 18013-7: de pago, en https://www.iso.org/. No se reproduce su contenido.
