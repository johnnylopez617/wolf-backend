from flask import Blueprint, redirect, url_for
from flask_security import current_user

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/admin')
    else:
        return redirect(url_for('security.login'))