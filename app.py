from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)
CORS(app)

# Use the path where Render mounts the secret file
cred = credentials.Certificate("/etc/secrets/firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com'
})

bucket = storage.bucket()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    blob = bucket.blob(f"uploads/{file.filename}")
    blob.upload_from_file(file)
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    blob = bucket.blob(f"uploads/{filename}")
    temp_file = f"/tmp/{filename}"
    blob.download_to_filename(temp_file)
    return send_file(temp_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
