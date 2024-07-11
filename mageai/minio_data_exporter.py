import pandas as pd
from io import BytesIO
from minio import Minio
import urllib3

# Define MinIO credentials and endpoint
access_key = 'minioroot'
secret_key = 'miniopassword'
minio_endpoint = 'filestorage:9000'  # Replace with your MinIO server endpoint
minio_bucket_name = 'olympicweightliftingbucket'

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    #df = pd.DataFrame(data)

    # Convert DataFrame to Parquet in memory
    parquet_buffer = BytesIO()
    data.to_parquet(parquet_buffer, index=False)

    # Connect to MinIO server
    try:
        client = Minio(minio_endpoint,
                    access_key=access_key,
                    secret_key=secret_key,
                    secure=False,
            )
            # Change to True if MinIO is using HTTPS

        # Check if bucket exists, create if not
        if not client.bucket_exists(minio_bucket_name):
            client.make_bucket(minio_bucket_name)

        # Upload CSV file to MinIO bucket
        parquet_buffer.seek(0)  # Reset file pointer
        object_name = 'athlete_events/athlete_events.parquet'
        client.put_object(minio_bucket_name, object_name, parquet_buffer, len(parquet_buffer.getvalue()))
        
        print(f"DataFrame successfully uploaded to MinIO bucket '{minio_bucket_name}' as '{object_name}'")

    except Exception as err:
        print(err)


