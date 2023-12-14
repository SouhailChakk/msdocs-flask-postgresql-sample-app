import os
from flask import Flask, request, redirect, url_for, Blueprint
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient



app2_bp = Blueprint('app2', __name__)
csrf = CSRFProtect(app)


def create_app():
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    # Configure Azure Storage
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

    return app

app = create_app()

@app2_bp.route('/upload', methods=['POST'])
@csrf.exempt
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)

        # Upload the file to Azure Blob Storage
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file.read(), overwrite=True)

        # Add additional logic, such as saving the blob URL to the database

        return 'File uploaded successfully'

        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
