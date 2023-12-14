# app2.py

import os
from flask import Blueprint, request, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from werkzeug.utils import secure_filename


app2_bp = Blueprint('app2', __name__)
csrf = CSRFProtect()

# Connect to Azure Storage Blob
connect_str = os.getenv('DefaultEndpointsProtocol=https;AccountName=csb10032000d733470a;AccountKey=7xF+CGBtqhNfWAoBCPQrp3cyp+qsDH+moJ9Np00KFNpkslSMNbuYW+/VzdHdxGdoZwMrDNgU5sKq+AStdVUzBQ==;EndpointSuffix=core.windows.net') 
container_name = "blobstorage"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)



try:
    container_client = blob_service_client.get_container_client(container=container_name)
    container_client.get_container_properties()
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name)

@csrf.exempt
@app2_bp.route('/upload_image/<int:id>', methods=['POST'])
def upload_image(id):
    # Ensure the 'customer_image' file is part of the form
    if 'customer_image' not in request.files:
        # Handle the case where no file is selected
        return redirect(url_for('app.details', id=id))

    file = request.files['customer_image']

    # Handle the case where the user submits an empty form
    if file.filename == '':
        return redirect(url_for('app.details', id=id))

    # Save the file to blob storage
    save_image_to_blob(file, id)

    return redirect(url_for('app.details', id=id))

def save_image_to_blob(file, restaurant_id):
    # Save the file to blob storage using the appropriate method
    # (you need to adapt this part based on your blob storage setup)
    filename = secure_filename(file.filename)  # Make sure to import secure_filename
    blob_client = container_client.get_blob_client(filename)

    # Upload the file to blob storage
    with file.stream as data:
        blob_client.upload_blob(data, overwrite=True)
