from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pymysql
import random

app = Flask(__name__)

# mysql database
# app.config['MYSQL_HOST'] = 'db-proy.chgqdjgci8b3.us-east-1.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = '24102066'
# app.config['MYSQL_DB'] = 'contactos_db'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'proyecto_cognitive'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/MAMP/tmp/mysql/mysql.sock'
mysql = MySQL(app)

app.secret_key='utec123'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/logout')
def logout():
    if session['logged_nombre'] is not None:
        session.clear()
        session['logged_nombre'] = None
        redirect('/login')
    else:
        redirect('/login')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if session['logged_nombre'] is not None:
            redirect('/conductores')
        else:
            return render_template('login.html')

@app.route('/login_val', methods=['POST'])
def login_val():
    if request.method == 'POST':
        name = request.form['name']
        clave = request.form['password']
        cur = mysql.connection.cursor()
        sentence = f"select * from centrales where nombre='{name}';"
        cur.execute(sentence)
        data = cur.fetchone()
        if (clave == data[4]):
            session.clear()
            session['logged_nombre'] = name
            return redirect('/conductores')

@app.route('/conductores')
def conductores():
    cur = mysql.connection.cursor()
    cur.execute('select * from conductores')
    data = cur.fetchall()
    return render_template('conductores.html', conductores=data)

@app.route('/new_conductor')
def new_conductor():
    return render_template('conductor_nuevo.html')

@app.route('/add_conductor', methods=['POST'])
def add_conductor():
    if request.method == 'POST':
        if session['logged_nombre'] is not None:
            nombre = request.form['name']
            apellido = request.form['lname']
            edad = request.form['edad']
            estatus = request.form['estatus']
            listaVocales = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            placa = ""
            for i in range(3):
                valor = random.randint(0,25)
                vocal = listaVocales[valor]
                placa = placa + vocal
            placa = placa + "-"
            for i in range(3):
                valor = str(random.randint(0,9))
                placa = placa + valor
            print(placa)
            cur = mysql.connection.cursor()
            sentence = f"insert into conductores (nombre, apellido, edad, cantidad_incidencias, estatus_conductor, placa_camion, nombre_central) values ('{nombre}', '{apellido}', {edad}, 0, {estatus}, '{placa}', '{session['logged_nombre']}');"
            cur.execute(sentence)
            mysql.connection.commit()
            return redirect('/conductores')
        else:
            return redirect('/login')

@app.route('/delete_conductor/<idCond>')
def delete_conductor(idCond):
    if session['logged_nombre'] is not None:
        cur = mysql.connection.cursor()
        sentence = f"delete from conductores where id_conductor = {idCond}"
        cur.execute(sentence)
        mysql.connection.commit()
        return redirect('/conductores')
    else:
        return redirect('/login')

@app.route('/edit_conductor/<idCond>', methods=['POST'])
def edit_conductor(idCond):
    if request.method == 'POST':
        if session['logged_nombre'] is not None:
            cur = mysql.connection.cursor()
            name = request.form['name']
            apellido = request.form['apellido']
            edad = request.form['edad']
            n_incidencias = request.form['cantidad_incidencias']
            estatus = request.form['estatus_conductor']
            sentence = f"update conductores set nombre = '{name}', apellido = '{apellido}', edad = {edad}, cantidad_incidencias = {n_incidencias}, estatus_conductor = {estatus} where id_conductor = {idCond};"
            cur.execute(sentence)
            mysql.connection.commit()
            return redirect('/conductores')
        else:
            return redirect('/login')


@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        hor = request.form['hora']
        ubi = request.form['ubicacion']
        pla = request.form['placa']
        print('INSERT', id, hor, ubi, pla)
        cur = mysql.connection.cursor()
        cur.execute('insert into incidentes(hora,ubicacion,placa) values(%s,%s,%s)', (hor, ubi, pla))
        mysql.connection.commit()
        flash('Contacto Insertado correctamente')
        return redirect(url_for('index'))


@app.route('/edit_cond/<id>')
def edit_cond(id):
    cur = mysql.connection.cursor()
    sentence = f"select * from conductores where id_conductor = {id};"
    cur.execute(sentence)
    data = cur.fetchone()
    return render_template('edit_conductor.html', conductores=data)

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from incidentes where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado correctamente')
    return redirect(url_for('index'))
    

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nom = request.form['nombres']
        tel = request.form['telefono']
        email = request.form['email']
        print('UPDATE', id, nom, tel, email)
        cur = mysql.connection.cursor()
        cur.execute("""
            update incidentes
            set nombres = %s,
                telefono = %s,
                email = %s
            where id = %s
        """,(nom, tel, email, id) )
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)