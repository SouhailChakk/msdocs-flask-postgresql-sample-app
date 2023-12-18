from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import datetime

app = Flask(__name__)

# Replace these values with your actual Azure Storage account details
account_name = 'blolbcontainer'
account_key = 'PLwcTYeojwwpUGEaDMJ3oHQ0dS5TJKvyJpyEAD1MBiLYf8qf82CvLCvknzWxvYIsbojEJaWbV4NN+AStxNiJxw=='
container_name = 'blobstorage'

blob_service_client = BlobServiceClient(account_url=f"https://blolbcontainer.blob.core.windows.net", credential=account_key)
container_client = blob_service_client.get_container_client(container_name)

@app.route('/upload_blob', methods=['POST'])
def upload_blob():
    try:
        # Get the file from the request
        file = request.files['file']

        # Ensure the file is present
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Generate a unique blob name using the current timestamp
        blob_name = f"customer_upload_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"

        # Get the Blob Client
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the image blob
        blob_client.upload_blob(file, blob_type="BlockBlob")

        return jsonify({"message": "Image uploaded successfully", "blob_name": blob_name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
