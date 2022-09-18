from flask_base import app
from flask import render_template
from flask_base.models.receta import Receta

@app.route('/recetas')
def recetas():
    return render_template('recetas/recetas.html', all_recetas = Receta.get_all_width_user())