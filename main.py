from flask import Flask, request, jsonify
import pymssql
import os

app = Flask(__name__)

# Cargar las credenciales de la base de datos desde las variables de entorno
server = os.getenv('SQL_SERVER', 'paselista.database.windows.net')
database = os.getenv('SQL_DATABASE', 'bbdPaseLista')
username = os.getenv('SQL_USER', 'adminsql')
password = os.getenv('SQL_PASSWORD', 'Paselista30')

def get_connection():
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
    return conn

# Ruta raíz para evitar el error 404
@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "Bienvenido a la API de Pase de Lista"}), 200

# El método POST crea información de asistencia
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

    try:
        cursor.execute(
            "INSERT INTO asistencia (id_estudiante, matricula, fecha, hora) VALUES (%d, %d, %s, %s)",
            (id_estudiante, matricula, fecha, hora)
        )
        conn.commit()
        return jsonify({"mensaje": "Asistencia registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
