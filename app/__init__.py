from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from config import config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
security = Security()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    
    from app import models
    
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security.init_app(app, user_datastore)
    
    from flask_admin.contrib.sqla import ModelView
    from flask_security import current_user
    
    class SecureModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated
        
        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('security.login'))
    
    from flask import redirect, url_for
    
    admin.add_view(SecureModelView(models.Game, db.session))
    admin.add_view(SecureModelView(models.SavedGameMeta, db.session))
    admin.add_view(SecureModelView(models.GameHoleData, db.session))
    admin.add_view(SecureModelView(models.GamePlayer, db.session))
    admin.add_view(SecureModelView(models.PlayerHoleScore, db.session))
    admin.add_view(SecureModelView(models.User, db.session))
    admin.add_view(SecureModelView(models.Role, db.session))
    
    from app.routes.index import index_bp
    from app.routes.games import games_bp
    from app.routes.saved_game_meta import saved_game_meta_bp
    from app.routes.game_hole_data import game_hole_data_bp
    from app.routes.game_players import game_players_bp
    from app.routes.player_hole_scores import player_hole_scores_bp
    
    app.register_blueprint(index_bp)
    app.register_blueprint(games_bp, url_prefix='/api')
    app.register_blueprint(saved_game_meta_bp, url_prefix='/api')
    app.register_blueprint(game_hole_data_bp, url_prefix='/api')
    app.register_blueprint(game_players_bp, url_prefix='/api')
    app.register_blueprint(player_hole_scores_bp, url_prefix='/api')
    
    return app
