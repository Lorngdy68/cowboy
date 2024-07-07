from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)
CORS(app)

# Path to your service account key file
cred = credentials.Certificate('/etc/secrets/firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://cowboy-storage.appspot.com'
})

bucket = storage.bucket()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    blob = bucket.blob(f'uploads/{file.filename}')
    blob.upload_from_file(file)
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    blob = bucket.blob(f'uploads/{filename}')
    if not blob.exists():
        return jsonify({'error': 'File not found'}), 404

    temp_file = f'/tmp/{filename}'
    blob.download_to_filename(temp_file)
    return send_file(temp_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
