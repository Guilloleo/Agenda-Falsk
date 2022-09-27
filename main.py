from flask import Flask, redirect, url_for, render_template, request, flash    
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

# Conexion DB
app.config['MYSQL_HOST'] = 'XXXXXX'
app.config['MYSQL_USER'] = 'XXXXX'    
app.config['MYSQL_PASSWORD'] = 'XXXXX'
app.config['MYSQL_DB'] = 'XXXXX'

mysql = MySQL(app)


# Listar
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contacto")
    contactos = cursor.fetchall()    
    cursor.close

    return render_template('index.html', contactos=contactos)


# Insertar
@app.route('/agregar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':

        nombres = request.form['nombres']
        correo = request.form['correo']
        telefono = request.form['telefono']        

        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO contacto VALUES(NULL, %s, %s, %s)", (nombres, correo, telefono))
        cursor.connection.commit()
        
        flash("Contacto Agregado!!!")

        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/actualizar/<contacto_id>', methods=['GET', 'POST'])
def actualizar(contacto_id):
    if request.method == 'POST':

        nombres = request.form['nombres']
        correo = request.form['correo']
        telefono = request.form['telefono']         

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contacto
            SET nombres = %s, 
                correo = %s,  
                telefono = %s
            WHERE id = %s
        """, (nombres, correo, telefono, contacto_id))
        cursor.connection.commit() 

        flash("Contacto Actualizado!!!")       

        return redirect(url_for('index'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contacto WHERE id = %s", (contacto_id,))
    contacto = cursor.fetchall()
    cursor.close

    return render_template('actualizar.html', contacto=contacto[0])



@app.route('/eliminar-dato/<contacto_id>')
def eliminar(contacto_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM contacto WHERE id = {contacto_id}")
    mysql.connection.commit()

    flash("Contacto Eliminado!!!")

    return redirect(url_for('index'))
    
@app.route('/acerca')
def about():
    return render_template('acerca.html')


if __name__ == '__main__':
    app.run(debug=True)
