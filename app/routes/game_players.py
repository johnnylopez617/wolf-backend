from flask import Blueprint, request, jsonify
from flask_security import auth_required
from app import db
from app.models import GamePlayer

game_players_bp = Blueprint('game_players', __name__)

@game_players_bp.route('/game-players', methods=['GET'])
@auth_required()
def get_game_players():
    players = GamePlayer.query.all()
    return jsonify([{
        'id': str(player.id),
        'game_id': str(player.game_id),
        'player_number': player.player_number,
        'player_name': player.player_name,
        'is_activated': player.is_activated,
        'handicap': player.handicap,
        'wolf_birdie_points': player.wolf_birdie_points,
        'wolf_eagle_points': player.wolf_eagle_points,
        'wolf_non_eagle_points': player.wolf_non_eagle_points,
        'non_wolf_birdie_points': player.non_wolf_birdie_points
    } for player in players])

@game_players_bp.route('/game-players/<player_id>', methods=['GET'])
@auth_required()
def get_game_player(player_id):
    player = GamePlayer.query.get_or_404(player_id)
    return jsonify({
        'id': str(player.id),
        'game_id': str(player.game_id),
        'player_number': player.player_number,
        'player_name': player.player_name,
        'is_activated': player.is_activated,
        'handicap': player.handicap,
        'wolf_birdie_points': player.wolf_birdie_points,
        'wolf_eagle_points': player.wolf_eagle_points,
        'wolf_non_eagle_points': player.wolf_non_eagle_points,
        'non_wolf_birdie_points': player.non_wolf_birdie_points
    })

@game_players_bp.route('/game-players', methods=['POST'])
@auth_required()
def create_game_player():
    data = request.json
    player = GamePlayer(
        game_id=data['game_id'],
        player_number=data['player_number'],
        player_name=data.get('player_name', ''),
        is_activated=data.get('is_activated', True),
        handicap=data.get('handicap', 0),
        wolf_birdie_points=data.get('wolf_birdie_points', 0),
        wolf_eagle_points=data.get('wolf_eagle_points', 0),
        wolf_non_eagle_points=data.get('wolf_non_eagle_points', 0),
        non_wolf_birdie_points=data.get('non_wolf_birdie_points', 0)
    )
    db.session.add(player)
    db.session.commit()
    return jsonify({'id': str(player.id)}), 201

@game_players_bp.route('/game-players/<player_id>', methods=['PUT'])
@auth_required()
def update_game_player(player_id):
    player = GamePlayer.query.get_or_404(player_id)
    data = request.json
    
    player.player_name = data.get('player_name', player.player_name)
    player.is_activated = data.get('is_activated', player.is_activated)
    player.handicap = data.get('handicap', player.handicap)
    player.wolf_birdie_points = data.get('wolf_birdie_points', player.wolf_birdie_points)
    player.wolf_eagle_points = data.get('wolf_eagle_points', player.wolf_eagle_points)
    player.wolf_non_eagle_points = data.get('wolf_non_eagle_points', player.wolf_non_eagle_points)
    player.non_wolf_birdie_points = data.get('non_wolf_birdie_points', player.non_wolf_birdie_points)
    
    db.session.commit()
    return jsonify({'message': 'GamePlayer updated successfully'})

@game_players_bp.route('/game-players/<player_id>', methods=['DELETE'])
@auth_required()
def delete_game_player(player_id):
    player = GamePlayer.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'GamePlayer deleted successfully'})