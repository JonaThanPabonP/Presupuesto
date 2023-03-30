from json import dumps
from bson import ObjectId
from flask import Flask, redirect, render_template, request, flash
from models import Movimiento
from pymongo import MongoClient
import locale,config

app = Flask(__name__)

# Conexión a mongodb
client = MongoClient(config.MONGO_URI)
app.config.from_object(config)
db = client.bgcbmv22klckam0

@app.route("/")
def index():
    gastos = 0
    ingresos = 0
    locale.setlocale(locale.LC_ALL, '')

    data_ingresos = db.Transacciones.find({"tipo":"Ingreso"})
    data_gastos = db.Transacciones.find({"tipo":"Gasto"})

    ingresos = sum([ingreso['monto'] for ingreso in data_ingresos])
    gastos = sum([gasto['monto'] for gasto in data_gastos])
    balance = ingresos - gastos

    return render_template('index.html', 
                           total_ingresos=f"${locale.format('%.0f', ingresos, grouping=True, monetary=True)}", 
                           total_gastos=f"${locale.format('%.0f', gastos, grouping=True, monetary=True)}", 
                           balance=f"${locale.format('%.0f', balance, grouping=True, monetary=True)}")


@app.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        tipo = request.form.get('tipo')
        categoria = request.form.get('categoria')
        detalle = request.form.get('detalle')
        monto = request.form.get('monto')
        
        nuevo_movimiento = Movimiento(fecha, tipo, categoria, detalle, monto)
        db.Transacciones.insert_one(nuevo_movimiento.nuevo())
        flash("Movimiento agregado exitosamente")
        return redirect('/movimientos');
    return render_template('add.html')


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    db.Transacciones.delete_one({'_id': ObjectId(id)})
    flash("Movimiento eliminado exitosamente")
    return redirect('/movimientos')


@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        tipo = request.form.get('tipo')
        categoria = request.form.get('categoria')
        detalle = request.form.get('detalle')
        monto = request.form.get('monto')

        actualiza_movimiento = Movimiento(fecha, tipo, categoria, detalle, monto)
        db.Transacciones.update_one({'_id':ObjectId(id)}, {'$set': actualiza_movimiento.editar()})
        flash("Movimiento actualizado exitosamente")
        return redirect('/movimientos')
    
    data_movimiento = db.Transacciones.find({'_id':ObjectId(id)}).next()
    categorias = db.Categorias.find()
    return render_template('edit.html', movimiento=data_movimiento, categorias=categorias)


@app.route("/movimientos")
def movimientos():
    tabla_ingresos = db.Transacciones.find({"tipo":"Ingreso"})
    tabla_gastos = db.Transacciones.find({"tipo":"Gasto"})
    return render_template("movimientos.html", tabla_ingresos=tabla_ingresos, tabla_gastos=tabla_gastos)


@app.route('/categorias_tipo/<tipo>')
def categorias_tipo(tipo):
    categorias = db.Categorias.find({'tipo': tipo})
    return dumps([{"nombre": cat["nombre"]} for cat in categorias])


if __name__ == "__main__":
    app.run(debug=True)