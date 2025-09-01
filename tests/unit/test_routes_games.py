import pytest

@pytest.mark.unit
class TestGamesRoutes:
    def test_get_games_requires_auth(self, client):
        response = client.get('/api/games')
        assert response.status_code == 302