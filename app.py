from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import random

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='Final',
    user='postgres',
    password='19283746abC',
    host='localhost'
)

@app.route('/')
def index():
    user = session.get('user')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, organizador, linkfoto FROM eventos')
    events = cursor.fetchall()
    cursor.close()
    return render_template('index.html', user=user, events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("entro en html")
    if request.method == 'POST':
        print("entro en post")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print("marco las variables")
        # Insert data into the Cuentas table
        cursor = conn.cursor()
        print("se conecto exitosamente")
        cursor.execute('INSERT INTO public."cuentas" (usuario, correo, contrasena) VALUES (%s, %s, %s)', (username, email, password))
        print("realizo el insert")
        conn.commit()
        cursor.close()
        print("llego al final")
        return redirect(url_for('index'))
    print("renderea como siempre")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        testt = username


        # Verifica si el usuario existe en la base de datos
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND contrasena = %s', (testt, password))
        user = cursor.fetchone()
        print("busca en la base de datos")
        cursor.close()

        if user:
            print("if user")
            session['user'] = {'username': user[0]}
            return redirect(url_for('index'))
        else:
            print("else not user")
            #return 'Nombre de usuario o contraseña incorrectos.'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/create_event', methods=['POST'])
def create_event():
    if 'user' in session and request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        # Insertar nuevo evento en la base de datos
    
        cursor = conn.cursor()
        cursor.execute('Select max(eventoid) From eventos')
        eventoid = cursor.fetchone()[0] + 1
        cursor.execute('INSERT INTO eventos (nombre, organizador, linkfoto, eventoid) VALUES (%s, %s, %s, %s)', (title, description, image, eventoid))
        conn.commit()
        cursor.close()

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)