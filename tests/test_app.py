"""Basic application tests."""


def test_homepage(client):
    """Homepage returns 200 and displays the platform title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"AuraNova" in response.data
    assert b"AI-Powered Healthcare" in response.data
