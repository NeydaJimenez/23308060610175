from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

@app.route('/clasificar_macro', methods=['GET', 'POST'])
def clasificar_macro():
    if 'alimentos_clasificados' not in session:
        session['alimentos_clasificados'] = []

    if request.method == 'POST':
        nombre = request.form['nombre']
        grasas = float(request.form['grasas'])
        proteinas = float(request.form['proteinas'])
        carbohidratos = float(request.form['carbohidratos'])

        cal_grasas = grasas * 9
        cal_proteinas = proteinas * 4
        cal_carbohidratos = carbohidratos * 4

        total_cal = cal_grasas + cal_proteinas + cal_carbohidratos

        porc_grasas = cal_grasas / total_cal * 100
        porc_proteinas = cal_proteinas / total_cal * 100
        porc_carbohidratos = cal_carbohidratos / total_cal * 100

        if porc_grasas >= porc_proteinas and porc_grasas >= porc_carbohidratos:
            clasificacion = 'Fuente de Grasas'
        elif porc_proteinas >= porc_grasas and porc_proteinas >= porc_carbohidratos:
            clasificacion = 'Fuente de Proteínas'
        else:
            clasificacion = 'Fuente de Carbohidratos'

        session['alimentos_clasificados'].append({
            'nombre': nombre,
            'clasificacion': clasificacion
        })
        session.modified = True

        return redirect(url_for('clasificar_macro'))

    return render_template('clasificar_macro.html', alimentos=session['alimentos_clasificados'])

@app.route('/resultados', methods=['GET', 'POST'])
def resultados():
    alimentos = session.get('alimentos_clasificados', [])
    return render_template('resultados.html', alimentos=alimentos)

@app.route('/limpiar', methods=['POST'])
def limpiar():
    session['alimentos_clasificados'] = []
    session.modified = True
    return redirect(url_for('resultados'))

if __name__ == '__main__':
    app.run(debug=True)