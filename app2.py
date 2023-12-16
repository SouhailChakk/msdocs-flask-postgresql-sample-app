from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
account_url = os.environ["https://csb10032000d733470a.blob.core.windows.net/"]

# create a credential 
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
)

app2_bp = Blueprint('app2', __name__)
csrf = CSRFProtect(app2_bp)

@csrf.exempt
@app2_bp.route('/upload_blob', methods=['POST'])
def upload_blob():
    local_dir = "static"
    container_name = 'csb10032000d733470a'

    # set client to access azure storage container
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)

    # get the container client
    container_client = blob_service_client.get_container_client(container=container_name)

    # read all files from directory
    filenames = os.listdir(local_dir)

    for filename in filenames:
        # get full file path
        full_file_path = os.path.join(local_dir, filename)

        # read files and upload data to blob storage container
        with open(full_file_path, "r") as fl:
            data = fl.read()
            container_client.upload_blob(name=filename, data=data)

    return redirect(url_for('index'))  # Assuming you have an 'index' route in your app

# Register the blueprint in your main app.py
from app2 import app2_bp

app.register_blueprint(app2_bp, url_prefix='/app2')

# main
if __name__ == "__main__":
    upload_blob()
