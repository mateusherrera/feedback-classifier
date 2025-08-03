"""
Views de dashborad privado para usuários autenticados.

:created by:    Mateus Herrera
:created on:    2025-08-03

:updated by:    Mateus Herrera
:updated on:    2025-08-03
"""

from flask import Blueprint, render_template


web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('login.html')

@web.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
