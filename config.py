"""
S3 connection
"""
import os
from pathlib import Path

import boto3
from cryptography.fernet import Fernet
from dotenv import load_dotenv

PATH_ROOT = Path(__file__).parents[0]
load_dotenv(Path(PATH_ROOT / '.env'))
FERNET = Fernet(b'JqDgNlXOMtUdu5ZYu5HQ0b3eCG0NzvMfWlz7a-aqz3c=')


def get_s3_resource() -> boto3.resource:
    """
    Resource to connect with S3.
    """
    return boto3.resource(
        's3',
        aws_access_key_id=os.getenv('S3_USER'),
        aws_secret_access_key=FERNET.decrypt(bytes(os.getenv('S3_PWD'), encoding='utf8')).decode(),
        endpoint_url=os.getenv('S3_HOST'),
        verify=os.getenv('CERTIFICATE')
    )
