from typing import Any
from typing import TypedDict


class KeycloakGroup(TypedDict, total=False):
    """Keycloak Group representation.

    ref: https://www.keycloak.org/docs-api/latest/rest-api/index.html#GroupRepresentation
    """

    id: str | None
    name: str | None
    description: str | None
    path: str | None
    parentId: str | None
    subGroupCount: int | None
    subGroups: list["KeycloakGroup"] | None
    attributes: dict[str, list[str]] | None
    realmRoles: list[str] | None
    clientRoles: dict[str, list[str]] | None
    access: dict[str, bool] | None


class KeycloakFederatedIdentity(TypedDict, total=False):
    """Keycloak Federated Identity representation.

    ref: https://www.keycloak.org/docs-api/latest/rest-api/index.html#FederatedIdentityRepresentation
    """

    identityProvider: str | None
    userId: str | None
    userName: str | None


class KeycloakUserConsent(TypedDict, total=False):
    """Keycloak UserConsent representation.

    ref: https://www.keycloak.org/docs-api/latest/rest-api/index.html#UserConsentRepresentation
    """

    clientId: str | None
    grantedClientScopes: list[str] | None
    createdDate: int | None
    lastUpdatedDate: int | None
    grantedRealmRoles: list[str] | None


class KeycloakUser(TypedDict, total=False):
    """Keycloak User representation.

    ref: https://www.keycloak.org/docs-api/latest/rest-api/index.html#UserRepresentation
    """

    id: str | None
    username: str | None
    firstName: str | None
    lastName: str | None
    email: str | None
    emailVerified: bool | None
    attributes: dict[str, list[str]] | None
    userProfileMetadata: dict[str, list[dict[str, list[str]]]] | None
    enabled: bool | None
    self: str | None
    origin: str | None
    createdTimestamp: int | None
    totp: bool | None
    federationLink: str | None
    serviceAccountClientId: str | None
    credentials: list[dict[str, Any]] | None
    disableableCredentialTypes: list[str] | None
    requiredActions: list[str] | None
    federatedIdentities: list[KeycloakFederatedIdentity] | None
    realmRoles: list[str] | None
    clientRoles: dict[str, list[str]] | None
    clientConsents: list[KeycloakUserConsent] | None
    notBefore: int | None
    applicationRoles: dict[str, list[str]] | None
    socialLinks: list[dict[str, str]] | None
    groups: list[str] | None
    access: dict[str, bool] | None
