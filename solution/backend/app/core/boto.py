from .config import config
import boto3

session = boto3.Session()

def get_boto():
    client = session.client(
        service_name='s3',
        endpoint_url=config.S3_ENDPOINT_URL,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    try:
        yield client
    except Exception:
        client.close()
