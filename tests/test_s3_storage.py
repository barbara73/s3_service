import shutil
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import boto3
from moto import mock_s3

from src.s3interactions.s3_download import S3Downloader
from src.s3interactions.s3_interactions import list_bucket_objects
from src.s3interactions.s3_storage import S3Storage
from tests.conftest import BUCKET_NAME, FILE_PATH, FILE_NAME, DOWNLOAD_PATH


@mock_s3
def test_upload_from_folder():
    """Test upload from folder."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    store = S3Storage(conn, BUCKET_NAME)
    store.upload_from_folder(FILE_PATH)
    assert list_bucket_objects(conn, BUCKET_NAME) == [FILE_NAME, 'other_file.txt']


@mock_s3
def test_upload_from_zip():
    """Test upload from folder."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    store = S3Storage(conn, BUCKET_NAME)
    store.upload_zip('zip_folder.zip')
    assert list_bucket_objects(conn, BUCKET_NAME) == ['zip_folder.zip']

    downloader = S3Downloader(conn, BUCKET_NAME)
    downloader.download_all_files(DOWNLOAD_PATH)
    with ZipFile(Path(DOWNLOAD_PATH, 'zip_folder.zip')) as zf:
        assert zf.namelist() == [FILE_NAME, 'other_file.txt']
    shutil.rmtree(DOWNLOAD_PATH)


@mock_s3
def test_upload_single_file():
    """Test upload single file."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    store = S3Storage(conn, BUCKET_NAME)
    store.upload_single_file(FILE_NAME, FILE_PATH)
    assert conn.Object(BUCKET_NAME, FILE_NAME).key == FILE_NAME


@mock_s3
def test_upload_in_memory_file():
    """Test upload of file in memory"""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    # content = 'blablabla'  # data in memory
    with BytesIO() as buffer:
        # add here the write of file (e.g. dcmwrite(buffer, content)
        buffer.seek(0)
        store = S3Storage(conn, BUCKET_NAME, buffer)
        store.upload_single_file('a_file_name.txt')

    assert list_bucket_objects(conn, BUCKET_NAME) == ['a_file_name.txt']
    body = conn.Object(BUCKET_NAME, 'a_file_name.txt').get()['Body'].read().decode("utf-8")
    assert body == ''
