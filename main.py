from flask import Flask, jsonify
from flask_cors import CORS  
import pymysql
import json  # Importar para decodificar JSON

app = Flask(__name__)
CORS(app)

# Configuración de conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'data'
}

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Conexión a la base de datos
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Consulta para obtener los datos
        cursor.execute("SELECT contenido FROM data LIMIT 1;")
        result = cursor.fetchone()

        if result:
            # Decodificar el string JSON almacenado en la base de datos
            contenido_json = json.loads(result[0])  # Decodifica el string a un objeto Python
            return jsonify({'contenido': contenido_json})  # Enviar como JSON válido
        else:
            return jsonify({'error': 'No se encontraron datos'}), 404

    except pymysql.MySQLError as sql_err:
        print(f"Error de MySQL: {sql_err}")
        return jsonify({'error': f'Error de MySQL: {sql_err}'}), 500

    except json.JSONDecodeError as json_err:
        print(f"Error al decodificar JSON: {json_err}")
        return jsonify({'error': f'Error al decodificar JSON: {json_err}'}), 500

    except Exception as e:
        print(f"Error desconocido: {e}")
        return jsonify({'error': f'Error desconocido: {e}'}), 500

    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
