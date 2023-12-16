from flask import request

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
        return f'Error: {str(ex)}'
