import pytest
import json

@pytest.mark.integration
class TestGameHoleDataJSONAPI:
    def test_create_hole_data_with_full_payload(self, authenticated_client):
        game_payload = {'game_name': 'Hole Data Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        hole_data_payload = {
            'game_id': game_id,
            'hole_number': 7,
            'hole_dollars': 4.5,
            'activated_dollars': 2.0,
            'pressed_count': True,
            'pressed_pushed_toggle': False,
            'alone_pushed': True,
            'roll_pushed': False,
            're_roll_pushed': True,
            'wolf_hole': 2,
            'hole_handicap': 3,
            'hole_par': 5,
            'prox_array': True
        }
        
        response = authenticated_client.post('/api/game-hole-data',
                             data=json.dumps(hole_data_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        hole_data_id = response_data['id']
        get_response = authenticated_client.get(f'/api/game-hole-data/{hole_data_id}')
        assert get_response.status_code == 200
        
        hole_data = json.loads(get_response.data)
        assert hole_data['game_id'] == game_id
        assert hole_data['hole_number'] == 7
        assert float(hole_data['hole_dollars']) == 4.5
        assert float(hole_data['activated_dollars']) == 2.0
        assert hole_data['pressed_count'] == True
        assert hole_data['pressed_pushed_toggle'] == False
        assert hole_data['alone_pushed'] == True
        assert hole_data['roll_pushed'] == False
        assert hole_data['re_roll_pushed'] == True
        assert hole_data['wolf_hole'] == 2
        assert hole_data['hole_handicap'] == 3
        assert hole_data['hole_par'] == 5
        assert hole_data['prox_array'] == True

    def test_create_hole_data_with_minimal_payload(self, authenticated_client):
        game_payload = {'game_name': 'Minimal Hole Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        minimal_payload = {
            'game_id': game_id,
            'hole_number': 3
        }
        
        response = authenticated_client.post('/api/game-hole-data',
                             data=json.dumps(minimal_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        hole_data_id = response_data['id']
        get_response = authenticated_client.get(f'/api/game-hole-data/{hole_data_id}')
        hole_data = json.loads(get_response.data)
        assert hole_data['hole_number'] == 3
        assert float(hole_data['hole_dollars']) == 2.0
        assert float(hole_data['activated_dollars']) == 0.0
        assert hole_data['hole_par'] == 4

    def test_update_hole_data_json_payload(self, authenticated_client):
        game_payload = {'game_name': 'Update Hole Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        hole_payload = {
            'game_id': game_id,
            'hole_number': 8,
            'hole_dollars': 3.0
        }
        create_response = authenticated_client.post('/api/game-hole-data',
                                   data=json.dumps(hole_payload),
                                   content_type='application/json')
        hole_data_id = json.loads(create_response.data)['id']
        
        update_payload = {
            'hole_dollars': 5.5,
            'activated_dollars': 3.0,
            'pressed_count': True,
            'wolf_hole': 1,
            'hole_par': 3
        }
        
        response = authenticated_client.put(f'/api/game-hole-data/{hole_data_id}',
                           data=json.dumps(update_payload),
                           content_type='application/json')
        
        assert response.status_code == 200
        update_response_data = json.loads(response.data)
        assert 'message' in update_response_data
        
        get_response = authenticated_client.get(f'/api/game-hole-data/{hole_data_id}')
        hole_data = json.loads(get_response.data)
        assert float(hole_data['hole_dollars']) == 5.5
        assert float(hole_data['activated_dollars']) == 3.0
        assert hole_data['pressed_count'] == True
        assert hole_data['wolf_hole'] == 1
        assert hole_data['hole_par'] == 3

    def test_hole_data_list_json_structure(self, authenticated_client):
        game_payload = {'game_name': 'Structure Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        hole_payload = {
            'game_id': game_id,
            'hole_number': 1,
            'hole_par': 4
        }
        authenticated_client.post('/api/game-hole-data',
                                data=json.dumps(hole_payload),
                                content_type='application/json')
        
        response = authenticated_client.get('/api/game-hole-data')
        assert response.status_code == 200
        
        hole_data_list = json.loads(response.data)
        assert isinstance(hole_data_list, list)
        assert len(hole_data_list) >= 1
        
        hole_data = hole_data_list[0]
        required_fields = [
            'id', 'game_id', 'hole_number', 'hole_dollars', 'activated_dollars',
            'pressed_count', 'pressed_pushed_toggle', 'alone_pushed', 'roll_pushed',
            're_roll_pushed', 'wolf_hole', 'hole_handicap', 'hole_par', 'prox_array'
        ]
        
        for field in required_fields:
            assert field in hole_data, f"Field {field} should be present in hole data JSON"

    def test_delete_hole_data_json_response(self, authenticated_client):
        game_payload = {'game_name': 'Delete Hole Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        hole_payload = {
            'game_id': game_id,
            'hole_number': 15
        }
        create_response = authenticated_client.post('/api/game-hole-data',
                                   data=json.dumps(hole_payload),
                                   content_type='application/json')
        hole_data_id = json.loads(create_response.data)['id']
        
        delete_response = authenticated_client.delete(f'/api/game-hole-data/{hole_data_id}')
        assert delete_response.status_code == 200
        
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['message'] == 'GameHoleData deleted successfully'