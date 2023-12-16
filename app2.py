import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob storage v12 - Python quickstart sample")
    # Quick start code goes here
except Exception as ex:
    print('Exception:')
    print(ex)

connect_str = "DefaultEndpointsProtocol=https;AccountName=csb10032000d733470a;AccountKey=7xF+CGBtqhNfWAoBCPQrp3cyp+qsDH+moJ9Np00KFNpkslSMNbuYW+/VzdHdxGdoZwMrDNgU5sKq+AStdVUzBQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = 'csb10032000d733470a'
container_client = blob_service_client.get_container_client(container_name)

# List the blobs in the container
print("\nListing blobs...")
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

def upload_image(id, customer_image):
    try:
        # Create a container client
        container_name = 'csb10032000d733470a'
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the image to Azure Blob Storage
        blob_name = f'review_images/{id}_{customer_image.filename}'
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(customer_image)

        return True
    except Exception as ex:
        print(f'Error: {str(ex)}')
        return False
