from flask import Blueprint, request, jsonify
from flask_security import auth_required
from app import db
from app.models import Game
from datetime import datetime
import uuid

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['GET'])
@auth_required()
def get_games():
    games = Game.query.all()
    return jsonify([{
        'id': str(game.id),
        'game_name': game.game_name,
        'hole': game.hole,
        'last_saved': game.last_saved.isoformat(),
        'dollars': float(game.dollars),
        'total_dollars': float(game.total_dollars),
        'is_continuing_game': game.is_continuing_game,
        'pressed_button': game.pressed_button,
        'wolf': game.wolf,
        'wolf_birdie_points': game.wolf_birdie_points,
        'wolf_eagle_points': game.wolf_eagle_points,
        'wolf_non_eagle_points': game.wolf_non_eagle_points,
        'non_wolf_birdie_points': game.non_wolf_birdie_points,
        'prox': game.prox,
        'created_at': game.created_at.isoformat(),
        'updated_at': game.updated_at.isoformat()
    } for game in games])

@games_bp.route('/games/<game_id>', methods=['GET'])
@auth_required()
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify({
        'id': str(game.id),
        'game_name': game.game_name,
        'hole': game.hole,
        'last_saved': game.last_saved.isoformat(),
        'dollars': float(game.dollars),
        'total_dollars': float(game.total_dollars),
        'is_continuing_game': game.is_continuing_game,
        'pressed_button': game.pressed_button,
        'wolf': game.wolf,
        'wolf_birdie_points': game.wolf_birdie_points,
        'wolf_eagle_points': game.wolf_eagle_points,
        'wolf_non_eagle_points': game.wolf_non_eagle_points,
        'non_wolf_birdie_points': game.non_wolf_birdie_points,
        'prox': game.prox,
        'created_at': game.created_at.isoformat(),
        'updated_at': game.updated_at.isoformat()
    })

@games_bp.route('/games', methods=['POST'])
@auth_required()
def create_game():
    data = request.json
    game = Game(
        game_name=data.get('game_name', 'New Game'),
        hole=data.get('hole', 0),
        dollars=data.get('dollars', 2.0),
        total_dollars=data.get('total_dollars', 0.0),
        is_continuing_game=data.get('is_continuing_game', True),
        pressed_button=data.get('pressed_button', 0),
        wolf=data.get('wolf', 0),
        wolf_birdie_points=data.get('wolf_birdie_points', 0),
        wolf_eagle_points=data.get('wolf_eagle_points', 0),
        wolf_non_eagle_points=data.get('wolf_non_eagle_points', 0),
        non_wolf_birdie_points=data.get('non_wolf_birdie_points', 0),
        prox=data.get('prox', 0)
    )
    db.session.add(game)
    db.session.commit()
    return jsonify({'id': str(game.id)}), 201

@games_bp.route('/games/<game_id>', methods=['PUT'])
@auth_required()
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.json
    
    game.game_name = data.get('game_name', game.game_name)
    game.hole = data.get('hole', game.hole)
    game.dollars = data.get('dollars', game.dollars)
    game.total_dollars = data.get('total_dollars', game.total_dollars)
    game.is_continuing_game = data.get('is_continuing_game', game.is_continuing_game)
    game.pressed_button = data.get('pressed_button', game.pressed_button)
    game.wolf = data.get('wolf', game.wolf)
    game.wolf_birdie_points = data.get('wolf_birdie_points', game.wolf_birdie_points)
    game.wolf_eagle_points = data.get('wolf_eagle_points', game.wolf_eagle_points)
    game.wolf_non_eagle_points = data.get('wolf_non_eagle_points', game.wolf_non_eagle_points)
    game.non_wolf_birdie_points = data.get('non_wolf_birdie_points', game.non_wolf_birdie_points)
    game.prox = data.get('prox', game.prox)
    game.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Game updated successfully'})

@games_bp.route('/games/<game_id>', methods=['DELETE'])
@auth_required()
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully'})