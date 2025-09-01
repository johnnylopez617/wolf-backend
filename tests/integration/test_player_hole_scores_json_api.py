import pytest
import json

@pytest.mark.integration
class TestPlayerHoleScoresJSONAPI:
    def test_create_player_hole_score_with_full_payload(self, authenticated_client):
        game_payload = {'game_name': 'Player Scores Test Game'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        score_payload = {
            'game_id': game_id,
            'player_number': 1,
            'hole_number': 9,
            'player_score': 3,
            'net_score': 2,
            'gross_score': 3,
            'player_money': 8.5,
            'wolf_score': 4,
            'prox_score': 1
        }
        
        response = authenticated_client.post('/api/player-hole-scores',
                             data=json.dumps(score_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        score_id = response_data['id']
        get_response = authenticated_client.get(f'/api/player-hole-scores/{score_id}')
        assert get_response.status_code == 200
        
        score_data = json.loads(get_response.data)
        assert score_data['game_id'] == game_id
        assert score_data['player_number'] == 1
        assert score_data['hole_number'] == 9
        assert score_data['player_score'] == 3
        assert score_data['net_score'] == 2
        assert score_data['gross_score'] == 3
        assert float(score_data['player_money']) == 8.5
        assert score_data['wolf_score'] == 4
        assert score_data['prox_score'] == 1

    def test_create_player_hole_score_with_minimal_payload(self, authenticated_client):
        game_payload = {'game_name': 'Minimal Score Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        minimal_payload = {
            'game_id': game_id,
            'player_number': 2,
            'hole_number': 4
        }
        
        response = authenticated_client.post('/api/player-hole-scores',
                             data=json.dumps(minimal_payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'id' in response_data
        
        score_id = response_data['id']
        get_response = authenticated_client.get(f'/api/player-hole-scores/{score_id}')
        score_data = json.loads(get_response.data)
        assert score_data['player_number'] == 2
        assert score_data['hole_number'] == 4
        assert score_data['player_score'] == 0
        assert score_data['net_score'] == 0
        assert float(score_data['player_money']) == 0.0

    def test_update_player_hole_score_json_payload(self, authenticated_client):
        game_payload = {'game_name': 'Update Score Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        score_payload = {
            'game_id': game_id,
            'player_number': 3,
            'hole_number': 12,
            'player_score': 5
        }
        create_response = authenticated_client.post('/api/player-hole-scores',
                                   data=json.dumps(score_payload),
                                   content_type='application/json')
        score_id = json.loads(create_response.data)['id']
        
        update_payload = {
            'player_score': 4,
            'net_score': 3,
            'gross_score': 4,
            'player_money': 12.0,
            'wolf_score': 2,
            'prox_score': 1
        }
        
        response = authenticated_client.put(f'/api/player-hole-scores/{score_id}',
                           data=json.dumps(update_payload),
                           content_type='application/json')
        
        assert response.status_code == 200
        update_response_data = json.loads(response.data)
        assert 'message' in update_response_data
        
        get_response = authenticated_client.get(f'/api/player-hole-scores/{score_id}')
        score_data = json.loads(get_response.data)
        assert score_data['player_score'] == 4
        assert score_data['net_score'] == 3
        assert score_data['gross_score'] == 4
        assert float(score_data['player_money']) == 12.0
        assert score_data['wolf_score'] == 2
        assert score_data['prox_score'] == 1

    def test_player_hole_scores_list_json_structure(self, authenticated_client):
        game_payload = {'game_name': 'Scores List Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        score_payload = {
            'game_id': game_id,
            'player_number': 1,
            'hole_number': 6,
            'player_score': 4
        }
        authenticated_client.post('/api/player-hole-scores',
                                data=json.dumps(score_payload),
                                content_type='application/json')
        
        response = authenticated_client.get('/api/player-hole-scores')
        assert response.status_code == 200
        
        scores_data = json.loads(response.data)
        assert isinstance(scores_data, list)
        assert len(scores_data) >= 1
        
        score = scores_data[0]
        required_fields = [
            'id', 'game_id', 'player_number', 'hole_number', 'player_score',
            'net_score', 'gross_score', 'player_money', 'wolf_score', 'prox_score'
        ]
        
        for field in required_fields:
            assert field in score, f"Field {field} should be present in score JSON"

    def test_delete_player_hole_score_json_response(self, authenticated_client):
        game_payload = {'game_name': 'Delete Score Test'}
        game_response = authenticated_client.post('/api/games',
                                 data=json.dumps(game_payload),
                                 content_type='application/json')
        game_id = json.loads(game_response.data)['id']
        
        score_payload = {
            'game_id': game_id,
            'player_number': 1,
            'hole_number': 18
        }
        create_response = authenticated_client.post('/api/player-hole-scores',
                                   data=json.dumps(score_payload),
                                   content_type='application/json')
        score_id = json.loads(create_response.data)['id']
        
        delete_response = authenticated_client.delete(f'/api/player-hole-scores/{score_id}')
        assert delete_response.status_code == 200
        
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['message'] == 'PlayerHoleScore deleted successfully'