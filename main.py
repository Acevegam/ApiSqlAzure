from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configura tu conexión a Azure SQL
server = 'paselista.database.windows.net'
database = 'bbdPaseLista'
username = 'adminsql'
password = 'Paselista30'  # Cambiar a tu contraseña real
driver = '{ODBC Driver 17 for SQL Server}'

def get_connection():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return conn

# El método POST crea información
@app.route('/asistencia', methods=['POST'])
def agregar_asistencia():
    data = request.get_json()
    
    # Validar que se proporcionen todos los datos necesarios
    if not all(key in data for key in ('id_estudiante', 'matricula', 'fecha', 'hora')):
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    id_estudiante = data['id_estudiante']
    matricula = data['matricula']
    fecha = data['fecha']
    hora = data['hora']
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asistencia (id_estudiante, matricula, fecha, hora) VALUES (?, ?, ?, ?)",
                   (id_estudiante, matricula, fecha, hora))
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": "Asistencia registrada exitosamente"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
