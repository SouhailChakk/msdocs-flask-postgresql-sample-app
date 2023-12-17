from flask import Flask, request, render_template, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Your Azure Storage Account connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=blolbcontainer;AccountKey=PLwcTYeojwwpUGEaDMJ3oHQ0dS5TJKvyJpyEAD1MBiLYf8qf82CvLCvknzWxvYIsbojEJaWbV4NN+AStxNiJxw==;EndpointSuffix=core.windows.net'

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Your Blob container name
container_name = 'blobstorage'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Get the uploaded file from the form
        customer_image = request.files['customer_image']

        # Create a container client
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the image to Azure Blob Storage
        blob_name = f'review_images/{customer_image.filename}'
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(customer_image)

        # Assuming you have a database, you can save the image reference there
        # Example: Save the blob URL to your PostgreSQL database
        # ...

        return 'Image uploaded successfully.'
    except Exception as ex:
        # Log the error for debugging purposes
        app.logger.error(f'Error during image upload: {str(ex)}')

        # Return a more informative error message to the client
        return f'Error during image upload: {str(ex)}'

if __name__ == '__main__':
    app.run(debug=True)
