from flask import Flask, render_template, request, session,jsonify, redirect, url_for
import psycopg2
import random
import json

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='Final',
    user='postgres',
    password='admin',
    host='localhost'
)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Aquí se agregarían las operaciones de suscripción en la base de datos
    session['subscribed'] = 'true'
    print("ahora suscrito")
    return jsonify(success=True)

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    # Aquí se agregarían las operaciones para cancelar la suscripción en la base de datos
    session['subscribed'] = 'false'
    print("ahora no suscrito")
    return jsonify(success=True)

@app.route('/')
def index():
    user = session.get('user')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, organizador, linkfoto, descripcion, fecha, duracion, ciudad, direccion FROM eventos')
    events = cursor.fetchall()
    cursor.execute('SELECT evento FROM atendimientos WHERE cuenta = %s', (user['username'],))
    asistir = cursor.fetchall()
    asistir = [item for sublist in asistir for item in sublist]
    session['asistir'] = asistir
    #print(user)
    print(asistir)
    cursor.close()
    #data_json = json.dumps(asistir)
    #return render_template('index.html', user=user, events=events, data_json=data_json)
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
        organizador = request.form['organizador']
        # Insertar nuevo evento en la base de datos
    
        cursor = conn.cursor()
        cursor.execute('Select max(eventoid), COUNT(*) as cantidadFilas From eventos')
        temp = cursor.fetchone()
        if temp[1] == 0:
            eventoid = 0
        else:
            eventoid = temp[0] + 1
        cursor.execute('INSERT INTO eventos (nombre, descripcion, linkfoto, eventoid, organizador) VALUES (%s, %s, %s, %s,%s)', (title, description, image, eventoid, organizador))
        conn.commit()
        cursor.close()

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)