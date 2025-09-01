import pytest
import json
import uuid
from datetime import datetime

@pytest.mark.integration
class TestSavedGameMetaJSONAPI:
    def test_create_saved_game_meta_with_full_payload(self, authenticated_client):
        game_payload = {'game_name': 'Saved Meta Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        meta_payload = {
            'id': game_id,
            'name': 'Championship Save',
            'saved_at': '2024-01-15T14:30:00',
            'hole': 9
        }
        
        response = authenticated_client.post('/api/saved-game-meta',
                             data=json.dumps(meta_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        meta_id = response_data['id']
        get_response = authenticated_client.get(f'/api/saved-game-meta/{meta_id}')
        assert get_response.status_code == 200
        
        meta_data = json.loads(get_response.data)
        assert meta_data['id'] == game_id
        assert meta_data['name'] == 'Championship Save'
        assert meta_data['saved_at'] == '2024-01-15T14:30:00'
        assert meta_data['hole'] == 9

    def test_update_saved_game_meta_json_payload(self, authenticated_client):
        game_payload = {'game_name': 'Update Meta Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        meta_payload = {
            'id': game_id,
            'name': 'Original Save',
            'saved_at': '2024-01-15T10:00:00',
            'hole': 5
        }
        create_response = authenticated_client.post('/api/saved-game-meta',
                                   data=json.dumps(meta_payload),
                                   content_type='application/json')
        meta_id = json.loads(create_response.data)['id']
        
        update_payload = {
            'name': 'Updated Save Name',
            'saved_at': '2024-01-15T16:45:00',
            'hole': 12
        }
        
        response = authenticated_client.put(f'/api/saved-game-meta/{meta_id}',
                           data=json.dumps(update_payload),
                           content_type='application/json')
        
        assert response.status_code == 200
        update_response_data = json.loads(response.data)
        assert 'message' in update_response_data
        
        get_response = authenticated_client.get(f'/api/saved-game-meta/{meta_id}')
        meta_data = json.loads(get_response.data)
        assert meta_data['name'] == 'Updated Save Name'
        assert meta_data['saved_at'] == '2024-01-15T16:45:00'
        assert meta_data['hole'] == 12

    def test_saved_game_meta_list_json_structure(self, authenticated_client):
        game_payload = {'game_name': 'Structure Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        meta_payload = {
            'id': game_id,
            'name': 'Test Save',
            'saved_at': '2024-01-15T12:00:00',
            'hole': 7
        }
        authenticated_client.post('/api/saved-game-meta',
                                data=json.dumps(meta_payload),
                                content_type='application/json')
        
        response = authenticated_client.get('/api/saved-game-meta')
        assert response.status_code == 200
        
        meta_list = json.loads(response.data)
        assert isinstance(meta_list, list)
        assert len(meta_list) >= 1
        
        meta = meta_list[0]
        required_fields = ['id', 'name', 'saved_at', 'hole']
        
        for field in required_fields:
            assert field in meta, f"Field {field} should be present in saved game meta JSON"

    def test_delete_saved_game_meta_json_response(self, authenticated_client):
        game_payload = {'game_name': 'Delete Meta Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        meta_payload = {
            'id': game_id,
            'name': 'Save to Delete',
            'saved_at': '2024-01-15T18:00:00',
            'hole': 3
        }
        create_response = authenticated_client.post('/api/saved-game-meta',
                                   data=json.dumps(meta_payload),
                                   content_type='application/json')
        meta_id = json.loads(create_response.data)['id']
        
        delete_response = authenticated_client.delete(f'/api/saved-game-meta/{meta_id}')
        assert delete_response.status_code == 200
        
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['message'] == 'SavedGameMeta deleted successfully'