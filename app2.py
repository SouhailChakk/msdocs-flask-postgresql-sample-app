from flask import Flask, request
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
app.config['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=csb10032000d733470a;AccountKey=7xF+CGBtqhNfWAoBCPQrp3cyp+qsDH+moJ9Np00KFNpkslSMNbuYW+/VzdHdxGdoZwMrDNgU5sKq+AStdVUzBQ==;EndpointSuffix=core.windows.net'

blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Get the uploaded file from the form
        customer_image = request.files['customer_image']

        # Create a container client
        container_name = 'blobstorage'
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the image to Azure Blob Storage
        blob_name = f'review_images/{customer_image.filename}'
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(customer_image)

        # Save the image reference in your PostgreSQL database
        # ...

        return 'Image uploaded successfully.'
    except Exception as ex:
        # Log the error for debugging purposes
        app.logger.error(f'Error during image upload: {str(ex)}')

        # Return a more informative error message to the client
        return f'Error during image upload: {str(ex)}'
