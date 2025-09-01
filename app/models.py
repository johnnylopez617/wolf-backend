from app import db
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_security import UserMixin, RoleMixin

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_name = db.Column(db.String(255), nullable=False, default='New Game')
    hole = db.Column(db.Integer, nullable=False, default=0)
    last_saved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    dollars = db.Column(db.Numeric(10, 2), nullable=False, default=2.0)
    total_dollars = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    is_continuing_game = db.Column(db.Boolean, nullable=False, default=True)
    
    pressed_button = db.Column(db.Integer, nullable=False, default=0)
    
    wolf = db.Column(db.Integer, nullable=False, default=0)
    wolf_birdie_points = db.Column(db.Integer, nullable=False, default=0)
    wolf_eagle_points = db.Column(db.Integer, nullable=False, default=0)
    wolf_non_eagle_points = db.Column(db.Integer, nullable=False, default=0)
    non_wolf_birdie_points = db.Column(db.Integer, nullable=False, default=0)
    
    prox = db.Column(db.Integer, nullable=False, default=0)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Game {self.game_name}>'


class SavedGameMeta(db.Model):
    __tablename__ = 'saved_game_meta'
    
    id = db.Column(UUID(as_uuid=True), db.ForeignKey('games.id', ondelete='CASCADE'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    saved_at = db.Column(db.DateTime, nullable=False)
    hole = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<SavedGameMeta {self.name}>'


class GameHoleData(db.Model):
    __tablename__ = 'game_hole_data'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    hole_number = db.Column(db.Integer, nullable=False)
    
    hole_dollars = db.Column(db.Numeric(10, 2), nullable=False, default=2.0)
    activated_dollars = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    
    pressed_count = db.Column(db.Boolean, nullable=False, default=False)
    pressed_pushed_toggle = db.Column(db.Boolean, nullable=False, default=False)
    alone_pushed = db.Column(db.Boolean, nullable=False, default=False)
    roll_pushed = db.Column(db.Boolean, nullable=False, default=False)
    re_roll_pushed = db.Column(db.Boolean, nullable=False, default=False)
    
    wolf_hole = db.Column(db.Integer, nullable=False, default=0)
    
    hole_handicap = db.Column(db.Integer, nullable=False, default=0)
    hole_par = db.Column(db.Integer, nullable=False, default=4)
    
    prox_array = db.Column(db.Boolean, nullable=False, default=False)
    
    __table_args__ = (
        db.CheckConstraint('hole_number >= 1 AND hole_number <= 18'),
        db.UniqueConstraint('game_id', 'hole_number'),
    )
    
    def __repr__(self):
        return f'<GameHoleData game_id={self.game_id} hole={self.hole_number}>'


class GamePlayer(db.Model):
    __tablename__ = 'game_players'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    player_number = db.Column(db.Integer, nullable=False)
    
    player_name = db.Column(db.String(255), nullable=False, default='')
    is_activated = db.Column(db.Boolean, nullable=False, default=True)
    handicap = db.Column(db.Integer, nullable=False, default=0)
    
    wolf_birdie_points = db.Column(db.Integer, nullable=False, default=0)
    wolf_eagle_points = db.Column(db.Integer, nullable=False, default=0)
    wolf_non_eagle_points = db.Column(db.Integer, nullable=False, default=0)
    non_wolf_birdie_points = db.Column(db.Integer, nullable=False, default=0)
    
    __table_args__ = (
        db.CheckConstraint('player_number >= 1 AND player_number <= 9'),
        db.UniqueConstraint('game_id', 'player_number'),
    )
    
    def __repr__(self):
        return f'<GamePlayer {self.player_name} #{self.player_number}>'


class PlayerHoleScore(db.Model):
    __tablename__ = 'player_hole_scores'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    player_number = db.Column(db.Integer, nullable=False)
    hole_number = db.Column(db.Integer, nullable=False)
    
    player_score = db.Column(db.Integer, nullable=False, default=0)
    net_score = db.Column(db.Integer, nullable=False, default=0)
    gross_score = db.Column(db.Integer, nullable=False, default=0)
    
    player_money = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    
    wolf_score = db.Column(db.Integer, nullable=False, default=0)
    
    prox_score = db.Column(db.Integer, nullable=False, default=0)
    
    __table_args__ = (
        db.CheckConstraint('player_number >= 1 AND player_number <= 9'),
        db.CheckConstraint('hole_number >= 1 AND hole_number <= 18'),
        db.UniqueConstraint('game_id', 'player_number', 'hole_number'),
    )
    
    def __repr__(self):
        return f'<PlayerHoleScore game_id={self.game_id} player={self.player_number} hole={self.hole_number}>'


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))