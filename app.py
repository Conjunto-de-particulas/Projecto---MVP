from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='Final',
    user='postgres',
    password='admin',
    host='localhost'
)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Insert data into the Cuentas table
        cursor = conn.cursor()
        cursor.execute('INSERT INTO public."Cuentas" (usuario, correo, contrasena) VALUES (%s, %s, %s)', (username, email, password))
        conn.commit()
        cursor.close()

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica si el usuario existe en la base de datos
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user'] = {'username': user[1]}
            return redirect(url_for('index'))
        else:
            return 'Nombre de usuario o contraseña incorrectos.'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)