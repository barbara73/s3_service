import sys
import pytest
from boto3 import resource
from moto.s3 import mock_s3

sys.path.append("../src")


BUCKET_NAME = 'MY_BUCKET_NAME'
FILE_NAME = 'file_name.csv'
FILE_PATH = 'files/s3_storage'
DOWNLOAD_PATH = 'files/s3_downloads'


@pytest.fixture
def empty_bucket():
    moto_fake = mock_s3()
    try:
        moto_fake.start()
        conn = resource('s3')
        conn.create_bucket(Bucket="OS_BUCKET")  # or the name of the bucket you use
        yield conn
    finally:
        moto_fake.stop()


if __name__ == '__main__':
    print(sys.path)
