from kitconcept.contentsync.converter import keycloak as converter

import pytest


@pytest.mark.parametrize(
    "key,expected",
    [
        ("@id", "/people/dtremea"),
        ("@type", "Person"),
        ("id", "dtremea"),
        ("first_name", "Dorneles"),
        ("last_name", "Tremea"),
        ("title", "Tremea, Dorneles"),
        ("email", "dtremea@plone.org"),
        ("location", "Garibaldi, Rio Grande do Sul, Brazil"),
        ("_transition", "publish"),
    ],
)
def test_converter_item(keycloak_user, key: str, expected: str):
    item_converter = converter.KeycloakPersonConverter("/people")
    converted = item_converter(keycloak_user)
    assert converted[key] == expected


def test_converter_item_blocks(keycloak_user):
    item_converter = converter.KeycloakPersonConverter("/people")
    converted = item_converter(keycloak_user)
    assert "blocks_layout" in converted
    blocks_layout = converted["blocks_layout"]["items"]
    assert len(blocks_layout) == 2
    assert "blocks" in converted
    assert converted["blocks"][blocks_layout[0]]["@type"] == "title"
    assert converted["blocks"][blocks_layout[1]]["@type"] == "slate"
