import pytest
import json



@pytest.mark.parametrize("route", [
    ("/recipes/1"),
    ("/recipes/"),
])
def test_recipe_get(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_recipe_post(client):
    response = client.post("/recipes", json={
        "title": "test 2",
        "description": "description body",
        "ingredients": "salt, water",
        "cooking_time": 30,
    })
    
    assert response.status_code == 200