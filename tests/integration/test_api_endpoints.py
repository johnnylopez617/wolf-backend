import pytest
import json

@pytest.mark.integration
class TestAPIEndpoints:
    def test_games_endpoints_require_auth(self, client):
        endpoints = [
            '/api/games',
            '/api/game-players', 
            '/api/game-hole-data',
            '/api/player-hole-scores',
            '/api/saved-game-meta'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 302, f"Endpoint {endpoint} should redirect unauthenticated users"

    def test_endpoints_exist_and_redirect_when_unauthenticated(self, client):
        endpoints = [
            '/api/games',
            '/api/game-players',
            '/api/game-hole-data', 
            '/api/player-hole-scores',
            '/api/saved-game-meta'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 302, f"Endpoint {endpoint} should redirect unauthenticated users"

    def test_post_endpoints_reject_unauthenticated_requests(self, client):
        endpoints = [
            '/api/games',
            '/api/game-players',
            '/api/game-hole-data',
            '/api/player-hole-scores',
            '/api/saved-game-meta'
        ]
        
        for endpoint in endpoints:
            response = client.post(endpoint, data='{}', content_type='application/json')
            assert response.status_code in [302, 401], f"POST to {endpoint} should reject unauthenticated requests"

    def test_root_redirects_to_login(self, client):
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location