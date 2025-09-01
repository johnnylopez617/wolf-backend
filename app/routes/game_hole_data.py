from flask import Blueprint, request, jsonify
from flask_security import auth_required
from app import db
from app.models import GameHoleData

game_hole_data_bp = Blueprint('game_hole_data', __name__)

@game_hole_data_bp.route('/game-hole-data', methods=['GET'])
@auth_required()
def get_game_hole_data():
    hole_data = GameHoleData.query.all()
    return jsonify([{
        'id': str(data.id),
        'game_id': str(data.game_id),
        'hole_number': data.hole_number,
        'hole_dollars': float(data.hole_dollars),
        'activated_dollars': float(data.activated_dollars),
        'pressed_count': data.pressed_count,
        'pressed_pushed_toggle': data.pressed_pushed_toggle,
        'alone_pushed': data.alone_pushed,
        'roll_pushed': data.roll_pushed,
        're_roll_pushed': data.re_roll_pushed,
        'wolf_hole': data.wolf_hole,
        'hole_handicap': data.hole_handicap,
        'hole_par': data.hole_par,
        'prox_array': data.prox_array
    } for data in hole_data])

@game_hole_data_bp.route('/game-hole-data/<data_id>', methods=['GET'])
@auth_required()
def get_game_hole_data_by_id(data_id):
    data = GameHoleData.query.get_or_404(data_id)
    return jsonify({
        'id': str(data.id),
        'game_id': str(data.game_id),
        'hole_number': data.hole_number,
        'hole_dollars': float(data.hole_dollars),
        'activated_dollars': float(data.activated_dollars),
        'pressed_count': data.pressed_count,
        'pressed_pushed_toggle': data.pressed_pushed_toggle,
        'alone_pushed': data.alone_pushed,
        'roll_pushed': data.roll_pushed,
        're_roll_pushed': data.re_roll_pushed,
        'wolf_hole': data.wolf_hole,
        'hole_handicap': data.hole_handicap,
        'hole_par': data.hole_par,
        'prox_array': data.prox_array
    })

@game_hole_data_bp.route('/game-hole-data', methods=['POST'])
@auth_required()
def create_game_hole_data():
    data = request.json
    hole_data = GameHoleData(
        game_id=data['game_id'],
        hole_number=data['hole_number'],
        hole_dollars=data.get('hole_dollars', 2.0),
        activated_dollars=data.get('activated_dollars', 0.0),
        pressed_count=data.get('pressed_count', False),
        pressed_pushed_toggle=data.get('pressed_pushed_toggle', False),
        alone_pushed=data.get('alone_pushed', False),
        roll_pushed=data.get('roll_pushed', False),
        re_roll_pushed=data.get('re_roll_pushed', False),
        wolf_hole=data.get('wolf_hole', 0),
        hole_handicap=data.get('hole_handicap', 0),
        hole_par=data.get('hole_par', 4),
        prox_array=data.get('prox_array', False)
    )
    db.session.add(hole_data)
    db.session.commit()
    return jsonify({'id': str(hole_data.id)}), 201

@game_hole_data_bp.route('/game-hole-data/<data_id>', methods=['PUT'])
@auth_required()
def update_game_hole_data(data_id):
    hole_data = GameHoleData.query.get_or_404(data_id)
    data = request.json
    
    hole_data.hole_dollars = data.get('hole_dollars', hole_data.hole_dollars)
    hole_data.activated_dollars = data.get('activated_dollars', hole_data.activated_dollars)
    hole_data.pressed_count = data.get('pressed_count', hole_data.pressed_count)
    hole_data.pressed_pushed_toggle = data.get('pressed_pushed_toggle', hole_data.pressed_pushed_toggle)
    hole_data.alone_pushed = data.get('alone_pushed', hole_data.alone_pushed)
    hole_data.roll_pushed = data.get('roll_pushed', hole_data.roll_pushed)
    hole_data.re_roll_pushed = data.get('re_roll_pushed', hole_data.re_roll_pushed)
    hole_data.wolf_hole = data.get('wolf_hole', hole_data.wolf_hole)
    hole_data.hole_handicap = data.get('hole_handicap', hole_data.hole_handicap)
    hole_data.hole_par = data.get('hole_par', hole_data.hole_par)
    hole_data.prox_array = data.get('prox_array', hole_data.prox_array)
    
    db.session.commit()
    return jsonify({'message': 'GameHoleData updated successfully'})

@game_hole_data_bp.route('/game-hole-data/<data_id>', methods=['DELETE'])
@auth_required()
def delete_game_hole_data(data_id):
    hole_data = GameHoleData.query.get_or_404(data_id)
    db.session.delete(hole_data)
    db.session.commit()
    return jsonify({'message': 'GameHoleData deleted successfully'})