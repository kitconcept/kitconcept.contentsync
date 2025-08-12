# syntax=docker/dockerfile:1.9
ARG KEYCLOAK_VERSION=26.2.4
FROM quay.io/keycloak/keycloak:$KEYCLOAK_VERSION AS builder

# Configure postgres database vendor
ENV KC_DB=postgres

# Enable features
ENV KC_FEATURES="token-exchange,scripts,admin-fine-grained-authz"

WORKDIR /opt/keycloak

# Build
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:$KEYCLOAK_VERSION

LABEL maintainer="kitconcept, GmbH <info@kitconcept.com>" \
      org.label-schema.name="Person Sync Keycloak" \
      org.label-schema.description="Test container used for person synchronization." \
      org.label-schema.vendor="kitconcept, GmbH"

COPY --from=builder /opt/keycloak/ /opt/keycloak/

USER root
RUN sed -i '/disabledAlgorithms/ s/ SHA1,//' /etc/crypto-policies/back-ends/java.config
USER keycloak

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
