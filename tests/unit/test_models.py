import pytest
from decimal import Decimal
from app.models import Game, GamePlayer, GameHoleData, PlayerHoleScore

@pytest.mark.unit
class TestGame:
    def test_game_creation(self):
        game = Game(game_name='Test Game', hole=5, dollars=Decimal('2.0'))
        assert game.game_name == 'Test Game'
        assert game.hole == 5
        assert game.dollars == Decimal('2.0')

    def test_game_attributes(self):
        game = Game(
            game_name='New Game',
            hole=0,
            dollars=Decimal('2.0'),
            total_dollars=Decimal('0.0'),
            is_continuing_game=True,
            pressed_button=0,
            wolf=0
        )
        assert game.game_name == 'New Game'
        assert game.hole == 0
        assert game.dollars == Decimal('2.0')
        assert game.total_dollars == Decimal('0.0')
        assert game.is_continuing_game == True
        assert game.pressed_button == 0
        assert game.wolf == 0

    def test_game_repr(self):
        game = Game(game_name='Wolf Championship')
        assert repr(game) == '<Game Wolf Championship>'

@pytest.mark.unit  
class TestGamePlayer:
    def test_game_player_creation(self):
        player = GamePlayer(
            player_number=1,
            player_name='John Doe',
            handicap=5,
            is_activated=True
        )
        assert player.player_name == 'John Doe'
        assert player.player_number == 1
        assert player.handicap == 5
        assert player.is_activated == True

    def test_game_player_attributes(self):
        player = GamePlayer(
            player_number=1,
            player_name='Test Player',
            is_activated=True,
            handicap=0,
            wolf_birdie_points=0,
            wolf_eagle_points=0
        )
        assert player.player_name == 'Test Player'
        assert player.is_activated == True
        assert player.handicap == 0
        assert player.wolf_birdie_points == 0
        assert player.wolf_eagle_points == 0

    def test_game_player_repr(self):
        player = GamePlayer(
            player_number=1,
            player_name='Jane Smith'
        )
        assert repr(player) == '<GamePlayer Jane Smith #1>'

@pytest.mark.unit
class TestGameHoleData:
    def test_game_hole_data_creation(self):
        hole_data = GameHoleData(
            hole_number=3,
            hole_dollars=Decimal('3.0'),
            hole_par=4
        )
        assert hole_data.hole_number == 3
        assert hole_data.hole_dollars == Decimal('3.0')
        assert hole_data.hole_par == 4

    def test_game_hole_data_attributes(self):
        hole_data = GameHoleData(
            hole_number=1,
            hole_dollars=Decimal('2.0'),
            activated_dollars=Decimal('0.0'),
            pressed_count=False,
            hole_handicap=0,
            hole_par=4
        )
        assert hole_data.hole_dollars == Decimal('2.0')
        assert hole_data.activated_dollars == Decimal('0.0')
        assert hole_data.pressed_count == False
        assert hole_data.hole_handicap == 0
        assert hole_data.hole_par == 4

@pytest.mark.unit
class TestPlayerHoleScore:
    def test_player_hole_score_creation(self):
        score = PlayerHoleScore(
            player_number=1,
            hole_number=5,
            player_score=4,
            net_score=3,
            gross_score=4
        )
        assert score.player_number == 1
        assert score.hole_number == 5
        assert score.player_score == 4
        assert score.net_score == 3
        assert score.gross_score == 4

    def test_player_hole_score_attributes(self):
        score = PlayerHoleScore(
            player_number=1,
            hole_number=1,
            player_score=0,
            net_score=0,
            gross_score=0,
            player_money=Decimal('0.0'),
            wolf_score=0,
            prox_score=0
        )
        assert score.player_score == 0
        assert score.net_score == 0
        assert score.gross_score == 0
        assert score.player_money == Decimal('0.0')
        assert score.wolf_score == 0
        assert score.prox_score == 0