from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('API_KEY_REMOVE_BG')

@app.route('/api/remove', methods=['GET'])
def remove_background():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "Image URL not provided"}), 400
    
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        data={"image_url": image_url, "size": "auto"},
        headers={"X-Api-Key": API_KEY},
    )
    
    if response.status_code == 200:
        # L'image avec l'arrière-plan supprimé est renvoyée sous forme de bytes
        return response.content, 200, {'Content-Type': 'image/png'}
    else:
        return jsonify({"error": response.json().get("errors", "Unknown error")}), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
