import pytest

@pytest.mark.integration  
class TestAPIIntegration:
    def test_app_starts(self, app):
        assert app is not None
        assert app.config['TESTING'] == True
    
    def test_app_has_routes(self, app):
        with app.app_context():
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            expected_routes = [
                '/api/games',
                '/api/game-players', 
                '/api/game-hole-data',
                '/api/player-hole-scores',
                '/api/saved-game-meta'
            ]
            for route in expected_routes:
                assert any(route in r for r in routes), f"Route {route} should be registered"