from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/recepcion', methods=['POST'])
def recepcion():
    # Obtiene los datos JSON enviados con la solicitud
    data = request.get_json()
    print(data)
    # Genera un nombre de archivo único para cada recepción
    # En un entorno de producción, considera usar un identificador más robusto
    filename = f"data_{request.remote_addr}_{request.headers.get('User-Agent')}.json".replace(" ", "_").replace("/", "_")
    
    # Guarda los datos en un archivo en el servidor
    with open(filename, 'a') as f:
        json.dump(data, f, indent=4)
    
    # Retorna una respuesta indicando el éxito de la operación
    return jsonify({"message": "Datos recibidos y guardados correctamente."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
