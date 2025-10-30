from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

alimentos = []

def calcular_calorias(grasas, proteinas, carbohidratos):
    return round(9*grasas + 4*proteinas + 4*carbohidratos, 2)

def determinar_clasificacion(grasas, proteinas, carbohidratos):
    if grasas >= proteinas and grasas >= carbohidratos:
        return 'Fuente de Grasas', 'Grasas'
    elif proteinas >= grasas and proteinas >= carbohidratos:
        return 'Fuente de Proteínas', 'Proteínas'
    elif carbohidratos >= grasas and carbohidratos >= proteinas:
        return 'Fuente de Carbohidratos', 'Carbohidratos'
    return '', ''

@app.route('/', methods=['GET', 'POST'])
def clasificar_macro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        grasas = float(request.form['grasas'])
        proteinas = float(request.form['proteinas'])
        carbohidratos = float(request.form['carbohidratos'])

        clasificacion, predominante = determinar_clasificacion(grasas, proteinas, carbohidratos)
        calorias = calcular_calorias(grasas, proteinas, carbohidratos)

        alimentos.append({
            'nombre': nombre,
            'grasas': grasas,
            'proteinas': proteinas,
            'carbohidratos': carbohidratos,
            'clasificacion': clasificacion,
            'predominante': predominante,
            'calorias': calorias
        })

    return render_template('clasificar_macro.html', alimentos=alimentos)

@app.route('/resultados')
def resultados():
    return render_template('resultados.html', alimentos=alimentos)

@app.route('/limpiar', methods=['POST'])
def limpiar():
    alimentos.clear()
    return redirect(url_for('clasificar_macro'))

if __name__ == '__main__':
    app.run(debug=True)