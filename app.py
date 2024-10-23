from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    iniciar_sesion()
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    iniciar_sesion()
    if request.method == 'POST':
        
        nuevo_producto = {
            'id': len(session['productos']) + 1,
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))

    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    iniciar_sesion()
    producto = next((prod for prod in session['productos'] if prod['id'] == id), None)
    
    if request.method == 'POST':
        if producto:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = int(request.form['cantidad'])
            producto['precio'] = float(request.form['precio'])
            producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
            producto['categoria'] = request.form['categoria']
            session.modified = True
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    iniciar_sesion()
    session['productos'] = [prod for prod in session['productos'] if prod['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)