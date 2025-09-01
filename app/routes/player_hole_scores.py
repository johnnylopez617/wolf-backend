from flask import Blueprint, request, jsonify
from flask_security import auth_required
from app import db
from app.models import PlayerHoleScore

player_hole_scores_bp = Blueprint('player_hole_scores', __name__)

@player_hole_scores_bp.route('/player-hole-scores', methods=['GET'])
@auth_required()
def get_player_hole_scores():
    scores = PlayerHoleScore.query.all()
    return jsonify([{
        'id': str(score.id),
        'game_id': str(score.game_id),
        'player_number': score.player_number,
        'hole_number': score.hole_number,
        'player_score': score.player_score,
        'net_score': score.net_score,
        'gross_score': score.gross_score,
        'player_money': float(score.player_money),
        'wolf_score': score.wolf_score,
        'prox_score': score.prox_score
    } for score in scores])

@player_hole_scores_bp.route('/player-hole-scores/<score_id>', methods=['GET'])
@auth_required()
def get_player_hole_score(score_id):
    score = PlayerHoleScore.query.get_or_404(score_id)
    return jsonify({
        'id': str(score.id),
        'game_id': str(score.game_id),
        'player_number': score.player_number,
        'hole_number': score.hole_number,
        'player_score': score.player_score,
        'net_score': score.net_score,
        'gross_score': score.gross_score,
        'player_money': float(score.player_money),
        'wolf_score': score.wolf_score,
        'prox_score': score.prox_score
    })

@player_hole_scores_bp.route('/player-hole-scores', methods=['POST'])
@auth_required()
def create_player_hole_score():
    data = request.json
    score = PlayerHoleScore(
        game_id=data['game_id'],
        player_number=data['player_number'],
        hole_number=data['hole_number'],
        player_score=data.get('player_score', 0),
        net_score=data.get('net_score', 0),
        gross_score=data.get('gross_score', 0),
        player_money=data.get('player_money', 0.0),
        wolf_score=data.get('wolf_score', 0),
        prox_score=data.get('prox_score', 0)
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({'id': str(score.id)}), 201

@player_hole_scores_bp.route('/player-hole-scores/<score_id>', methods=['PUT'])
@auth_required()
def update_player_hole_score(score_id):
    score = PlayerHoleScore.query.get_or_404(score_id)
    data = request.json
    
    score.player_score = data.get('player_score', score.player_score)
    score.net_score = data.get('net_score', score.net_score)
    score.gross_score = data.get('gross_score', score.gross_score)
    score.player_money = data.get('player_money', score.player_money)
    score.wolf_score = data.get('wolf_score', score.wolf_score)
    score.prox_score = data.get('prox_score', score.prox_score)
    
    db.session.commit()
    return jsonify({'message': 'PlayerHoleScore updated successfully'})

@player_hole_scores_bp.route('/player-hole-scores/<score_id>', methods=['DELETE'])
@auth_required()
def delete_player_hole_score(score_id):
    score = PlayerHoleScore.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return jsonify({'message': 'PlayerHoleScore deleted successfully'})