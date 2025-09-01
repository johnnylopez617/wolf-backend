import pytest
import json
import uuid

@pytest.mark.integration
class TestGamePlayersJSONAPI:
    def test_create_game_player_with_full_payload(self, authenticated_client):
        game_payload = {'game_name': 'Test Game for Players'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        player_payload = {
            'game_id': game_id,
            'player_number': 1,
            'player_name': 'Tiger Woods',
            'is_activated': True,
            'handicap': 5,
            'wolf_birdie_points': 3,
            'wolf_eagle_points': 6,
            'wolf_non_eagle_points': 1,
            'non_wolf_birdie_points': 2
        }
        
        response = authenticated_client.post('/api/game-players',
                             data=json.dumps(player_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        player_id = response_data['id']
        get_response = authenticated_client.get(f'/api/game-players/{player_id}')
        assert get_response.status_code == 200
        
        player_data = json.loads(get_response.data)
        assert player_data['game_id'] == game_id
        assert player_data['player_number'] == 1
        assert player_data['player_name'] == 'Tiger Woods'
        assert player_data['is_activated'] == True
        assert player_data['handicap'] == 5
        assert player_data['wolf_birdie_points'] == 3
        assert player_data['wolf_eagle_points'] == 6
        assert player_data['wolf_non_eagle_points'] == 1
        assert player_data['non_wolf_birdie_points'] == 2

    def test_create_game_player_with_minimal_payload(self, authenticated_client):
        game_payload = {'game_name': 'Minimal Player Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        minimal_player_payload = {
            'game_id': game_id,
            'player_number': 2
        }
        
        response = authenticated_client.post('/api/game-players',
                             data=json.dumps(minimal_player_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        player_id = response_data['id']
        get_response = authenticated_client.get(f'/api/game-players/{player_id}')
        player_data = json.loads(get_response.data)
        assert player_data['player_number'] == 2
        assert player_data['player_name'] == ''
        assert player_data['is_activated'] == True
        assert player_data['handicap'] == 0

    def test_update_game_player_json_payload(self, authenticated_client):
        game_payload = {'game_name': 'Update Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        player_payload = {
            'game_id': game_id,
            'player_number': 1,
            'player_name': 'Original Name'
        }
        create_response = authenticated_client.post('/api/game-players',
                                   data=json.dumps(player_payload),
                                   content_type='application/json')
        player_id = json.loads(create_response.data)['id']
        
        update_payload = {
            'player_name': 'Updated Champion',
            'handicap': 12,
            'wolf_birdie_points': 5,
            'is_activated': False
        }
        
        response = authenticated_client.put(f'/api/game-players/{player_id}',
                           data=json.dumps(update_payload),
                           content_type='application/json')
        
        assert response.status_code == 200
        update_response_data = json.loads(response.data)
        assert 'message' in update_response_data
        
        get_response = authenticated_client.get(f'/api/game-players/{player_id}')
        player_data = json.loads(get_response.data)
        assert player_data['player_name'] == 'Updated Champion'
        assert player_data['handicap'] == 12
        assert player_data['wolf_birdie_points'] == 5
        assert player_data['is_activated'] == False

    def test_game_players_list_json_structure(self, authenticated_client):
        game_payload = {'game_name': 'List Structure Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        player_payload = {
            'game_id': game_id,
            'player_number': 1,
            'player_name': 'Test Player'
        }
        authenticated_client.post('/api/game-players',
                                data=json.dumps(player_payload),
                                content_type='application/json')
        
        response = authenticated_client.get('/api/game-players')
        assert response.status_code == 200
        
        players_data = json.loads(response.data)
        assert isinstance(players_data, list)
        assert len(players_data) >= 1
        
        player = players_data[0]
        required_fields = [
            'id', 'game_id', 'player_number', 'player_name', 'is_activated',
            'handicap', 'wolf_birdie_points', 'wolf_eagle_points',
            'wolf_non_eagle_points', 'non_wolf_birdie_points'
        ]
        
        for field in required_fields:
            assert field in player, f"Field {field} should be present in player JSON"

    def test_delete_game_player_json_response(self, authenticated_client):
        game_payload = {'game_name': 'Delete Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        player_payload = {
            'game_id': game_id,
            'player_number': 1,
            'player_name': 'Player to Delete'
        }
        create_response = authenticated_client.post('/api/game-players',
                                   data=json.dumps(player_payload),
                                   content_type='application/json')
        player_id = json.loads(create_response.data)['id']
        
        delete_response = authenticated_client.delete(f'/api/game-players/{player_id}')
        assert delete_response.status_code == 200
        
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['message'] == 'GamePlayer deleted successfully'