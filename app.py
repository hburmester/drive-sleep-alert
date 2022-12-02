from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pymysql

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

@app.route('/login')
def login():
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

@app.route('/add_conductor')
def add_conductor():
    if session['logged_nombre'] is not None:
        print(session['logged_nombre'])


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
    

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from incidentes where id = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', contacto=data[0])

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