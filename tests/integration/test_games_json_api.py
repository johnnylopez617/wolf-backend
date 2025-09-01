import pytest
import json
import uuid
from decimal import Decimal

@pytest.mark.integration
class TestGamesJSONAPI:
    def test_create_game_with_full_payload(self, authenticated_client):
        game_payload = {
            'game_name': 'Championship Round',
            'hole': 5,
            'dollars': 3.5,
            'total_dollars': 17.5,
            'is_continuing_game': True,
            'pressed_button': 2,
            'wolf': 3,
            'wolf_birdie_points': 4,
            'wolf_eagle_points': 8,
            'wolf_non_eagle_points': 2,
            'non_wolf_birdie_points': 3,
            'prox': 1
        }
        
        response = authenticated_client.post('/api/games',
                             data=json.dumps(game_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        game_id = response_data['id']
        get_response = authenticated_client.get(f'/api/games/{game_id}')
        assert get_response.status_code == 200
        
        game_data = json.loads(get_response.data)
        assert game_data['game_name'] == 'Championship Round'
        assert game_data['hole'] == 5
        assert float(game_data['dollars']) == 3.5
        assert float(game_data['total_dollars']) == 17.5
        assert game_data['is_continuing_game'] == True
        assert game_data['pressed_button'] == 2
        assert game_data['wolf'] == 3
        assert game_data['wolf_birdie_points'] == 4
        assert game_data['wolf_eagle_points'] == 8
        assert game_data['wolf_non_eagle_points'] == 2
        assert game_data['non_wolf_birdie_points'] == 3
        assert game_data['prox'] == 1

    def test_create_game_with_minimal_payload(self, authenticated_client):
        minimal_payload = {
            'game_name': 'Quick Game'
        }
        
        response = authenticated_client.post('/api/games',
                             data=json.dumps(minimal_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        game_id = response_data['id']
        get_response = authenticated_client.get(f'/api/games/{game_id}')
        assert get_response.status_code == 200
        
        game_data = json.loads(get_response.data)
        assert game_data['game_name'] == 'Quick Game'
        assert game_data['hole'] == 0
        assert float(game_data['dollars']) == 2.0
        assert float(game_data['total_dollars']) == 0.0
        assert game_data['is_continuing_game'] == True

    def test_update_game_with_partial_payload(self, authenticated_client):
        create_payload = {
            'game_name': 'Original Game',
            'hole': 1,
            'dollars': 2.0
        }
        
        create_response = authenticated_client.post('/api/games',
                                   data=json.dumps(create_payload),
                                   content_type='application/json')
        game_id = json.loads(create_response.data)['id']
        
        update_payload = {
            'game_name': 'Updated Championship',
            'hole': 12,
            'total_dollars': 45.0,
            'wolf': 2
        }
        
        response = authenticated_client.put(f'/api/games/{game_id}',
                           data=json.dumps(update_payload),
                           content_type='application/json')
        
        assert response.status_code == 200
        update_response_data = json.loads(response.data)
        assert 'message' in update_response_data
        
        get_response = authenticated_client.get(f'/api/games/{game_id}')
        game_data = json.loads(get_response.data)
        assert game_data['game_name'] == 'Updated Championship'
        assert game_data['hole'] == 12
        assert float(game_data['total_dollars']) == 45.0
        assert game_data['wolf'] == 2
        assert float(game_data['dollars']) == 2.0

    def test_games_list_json_structure(self, authenticated_client):
        create_payload = {'game_name': 'List Test Game'}
        authenticated_client.post('/api/games',
                                data=json.dumps(create_payload),
                                content_type='application/json')
        
        response = authenticated_client.get('/api/games')
        assert response.status_code == 200
        
        games_data = json.loads(response.data)
        assert isinstance(games_data, list)
        assert len(games_data) >= 1
        
        game = games_data[0]
        required_fields = [
            'id', 'game_name', 'hole', 'last_saved', 'dollars', 'total_dollars',
            'is_continuing_game', 'pressed_button', 'wolf', 'wolf_birdie_points',
            'wolf_eagle_points', 'wolf_non_eagle_points', 'non_wolf_birdie_points',
            'prox', 'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert field in game, f"Field {field} should be present in game JSON"

    def test_delete_game_json_response(self, authenticated_client):
        create_payload = {'game_name': 'Game to Delete'}
        create_response = authenticated_client.post('/api/games',
                                   data=json.dumps(create_payload),
                                   content_type='application/json')
        game_id = json.loads(create_response.data)['id']
        
        delete_response = authenticated_client.delete(f'/api/games/{game_id}')
        assert delete_response.status_code == 200
        
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['message'] == 'Game deleted successfully'