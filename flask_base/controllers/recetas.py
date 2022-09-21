from flask_base import app
from flask import render_template, redirect, request, flash, session
from flask_base.models.receta import Receta
from flask_base.models.usuario import Usuario

@app.route('/recetas')
def recetas():
    if 'usuarios_id' not in session:
        return redirect('/login')
    return render_template('recetas/recetas.html', all_recetas = Receta.get_all_width_user())

@app.route('/recetas/nuevo')
def nueva_receta():
    if 'usuarios_id' not in session:
        return redirect('/login')
    return render_template('recetas/crearReceta.html')

@app.route('/procesar_receta', methods=['POST'])
def procesar_receta():
    
    print(request.form)
    if not Receta.validar(request.form):
        return redirect('/recetas/nuevo')

    nueva_receta={
        'nombre':request.form['nombre'],
        'descripcion':request.form['descripcion'],
        'instrucciones':request.form['instrucciones'],
        'fecha_elaboracion':request.form['fecha_elaboracion'],
        'menos_30':request.form['menos_30'],
        'usuarios_id':session['usuarios_id']
    }
    receta=Receta.save(nueva_receta)
    if receta == False:
        flash('algo errado paso con la creacion de la receta', 'error')
        return redirect ('/recetas/nuevo')
    print(receta)
    return redirect('/recetas')

@app.route('/recetas/editar/<int:id>')
def editar_receta(id):
    if 'usuarios_id' not in session:
        return redirect('/login')
    receta=Receta.get_by_id_user(id)[0]
    if session['usuarios_id'] == receta.usuario_id:
        receta.fecha_elaboracion = receta.fecha_elaboracion.strftime("%Y-%m-%d")
        return render_template('recetas/editarReceta.html',receta=receta)
    return redirect(f'/recetas/{id}')

@app.route('/procesar/editar/recetas/<int:id>', methods=['POST'])
def procesar_editar_receta(id):
    print(request.form)
    if not Receta.validar(request.form):
        return redirect('/recetas/nuevo')
    
    actualizar_receta= {
        'id':id,
        'nombre':request.form['nombre'],
        'descripcion':request.form['descripcion'],
        'instrucciones':request.form['instrucciones'],
        'fecha_elaboracion':request.form['fecha_elaboracion'],
        'menos_30':request.form['menos_30'],
    }
    actualizar = Receta.update(actualizar_receta)
    print("QUIERO VER ACTUALIZAR--->",actualizar)
    return redirect('/recetas')

@app.route('/recetas/eliminar/<id>', methods=['GET'])
def recetas_eliminar_procesar(id):
    if 'usuarios_id' not in session:
        return redirect('/login')
    receta=Receta.get_by_id_user(id)[0]
    if session['usuarios_id'] == receta.usuario_id:
        Receta.delete(id)
        flash(f"exito al eliminar la ciudad","success")
        return redirect('/recetas')
    return redirect('/recetas')


@app.route('/recetas/<id>')
def recetas_detalle(id):
    if 'usuarios_id' not in session:
        return redirect('/login')
    receta = Receta.view_by_id(id)
    receta.fecha_elaboracion = receta.fecha_elaboracion.strftime('%Y-%m-%d')
    return render_template('recetas/detalleRecetas.html', receta = receta)