import pytest
from conftest import create_test_app, db
from config import config

@pytest.mark.unit
class TestAppFactory:
    def test_create_test_app_config(self):
        app = create_test_app()
        assert app.config['TESTING'] == True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
        assert app.config['WTF_CSRF_ENABLED'] == False

    def test_blueprints_registered(self):
        app = create_test_app()
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        expected_blueprints = ['index', 'games', 'saved_game_meta', 'game_hole_data', 'game_players', 'player_hole_scores']
        for bp_name in expected_blueprints:
            assert bp_name in blueprint_names

    def test_app_has_database(self):
        app = create_test_app()
        with app.app_context():
            assert db.engine is not None