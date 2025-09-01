from flask import Blueprint, request, jsonify
from flask_security import auth_required
from app import db
from app.models import SavedGameMeta

saved_game_meta_bp = Blueprint('saved_game_meta', __name__)

@saved_game_meta_bp.route('/saved-game-meta', methods=['GET'])
@auth_required()
def get_saved_game_meta():
    metas = SavedGameMeta.query.all()
    return jsonify([{
        'id': str(meta.id),
        'name': meta.name,
        'saved_at': meta.saved_at.isoformat(),
        'hole': meta.hole
    } for meta in metas])

@saved_game_meta_bp.route('/saved-game-meta/<meta_id>', methods=['GET'])
@auth_required()
def get_saved_game_meta_by_id(meta_id):
    meta = SavedGameMeta.query.get_or_404(meta_id)
    return jsonify({
        'id': str(meta.id),
        'name': meta.name,
        'saved_at': meta.saved_at.isoformat(),
        'hole': meta.hole
    })

@saved_game_meta_bp.route('/saved-game-meta', methods=['POST'])
@auth_required()
def create_saved_game_meta():
    data = request.json
    meta = SavedGameMeta(
        id=data['id'],
        name=data['name'],
        saved_at=data['saved_at'],
        hole=data['hole']
    )
    db.session.add(meta)
    db.session.commit()
    return jsonify({'id': str(meta.id)}), 201

@saved_game_meta_bp.route('/saved-game-meta/<meta_id>', methods=['PUT'])
@auth_required()
def update_saved_game_meta(meta_id):
    meta = SavedGameMeta.query.get_or_404(meta_id)
    data = request.json
    
    meta.name = data.get('name', meta.name)
    meta.saved_at = data.get('saved_at', meta.saved_at)
    meta.hole = data.get('hole', meta.hole)
    
    db.session.commit()
    return jsonify({'message': 'SavedGameMeta updated successfully'})

@saved_game_meta_bp.route('/saved-game-meta/<meta_id>', methods=['DELETE'])
@auth_required()
def delete_saved_game_meta(meta_id):
    meta = SavedGameMeta.query.get_or_404(meta_id)
    db.session.delete(meta)
    db.session.commit()
    return jsonify({'message': 'SavedGameMeta deleted successfully'})