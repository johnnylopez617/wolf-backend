import pytest
import tempfile
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from app.models import User, Role, Game, GamePlayer, GameHoleData, PlayerHoleScore, SavedGameMeta
from config import TestingConfig

db = SQLAlchemy()

def create_test_app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    
    db.init_app(app)
    
    from app import models
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)
    
    from app.routes.index import index_bp
    from app.routes.games import games_bp
    from app.routes.saved_game_meta import saved_game_meta_bp
    from app.routes.game_hole_data import game_hole_data_bp
    from app.routes.game_players import game_players_bp
    from app.routes.player_hole_scores import player_hole_scores_bp
    
    app.register_blueprint(index_bp)
    app.register_blueprint(games_bp, url_prefix='/api')
    app.register_blueprint(saved_game_meta_bp, url_prefix='/api')
    app.register_blueprint(game_hole_data_bp, url_prefix='/api')
    app.register_blueprint(game_players_bp, url_prefix='/api')
    app.register_blueprint(player_hole_scores_bp, url_prefix='/api')
    
    return app

@pytest.fixture
def app():
    app = create_test_app()
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_headers():
    return {'Content-Type': 'application/json'}

@pytest.fixture
def test_user(app):
    with app.app_context():
        from flask_security import hash_password
        role = Role(name='user', description='User role')
        user = User(
            email='test@example.com',
            password=hash_password('password123'),
            active=True,
            fs_uniquifier='test-unique'
        )
        user.roles.append(role)
        db.session.add(role)
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture  
def authenticated_client(app, client):
    with app.app_context():
        from flask_security import hash_password
        role = Role(name='user', description='User role')
        user = User(
            email='test@example.com',
            password=hash_password('password123'),
            active=True,
            fs_uniquifier='test-unique-auth'
        )
        user.roles.append(role)
        db.session.add(role)
        db.session.add(user)
        db.session.commit()
        
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        return client

@pytest.fixture
def sample_game():
    return {
        'game_name': 'Test Game',
        'hole': 1,
        'dollars': 5.0,
        'total_dollars': 10.0,
        'is_continuing_game': True,
        'pressed_button': 0,
        'wolf': 1,
        'wolf_birdie_points': 2,
        'wolf_eagle_points': 4,
        'wolf_non_eagle_points': 1,
        'non_wolf_birdie_points': 1,
        'prox': 0
    }