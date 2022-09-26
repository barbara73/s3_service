import os
import shutil
from pathlib import Path
from zipfile import ZipFile

import boto3
from moto import mock_s3

from src.s3interactions.s3_download import S3Downloader
from src.s3interactions.s3_storage import S3Storage
from tests.conftest import BUCKET_NAME, FILE_NAME, FILE_PATH, DOWNLOAD_PATH, PATH_ROOT


@mock_s3
def test_download_single_file():
    """Test download of single file."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    obj = conn.Object(bucket_name=BUCKET_NAME,
                      key=FILE_NAME)
    obj.upload_file(Filename=str(Path(FILE_PATH, FILE_NAME)))
    downloader = S3Downloader(conn, BUCKET_NAME)
    downloader.download_single_file(FILE_NAME, str(DOWNLOAD_PATH))

    for filename in os.listdir(DOWNLOAD_PATH):
        assert filename == 'file_name.csv'
        shutil.rmtree(DOWNLOAD_PATH)


@mock_s3
def test_my_model_save():
    """
    Test can save into body.
    Not yet used!
    """
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    store = S3Storage(conn, BUCKET_NAME)
    store.upload_single_file(FILE_NAME, FILE_PATH)
    body = conn.Object(BUCKET_NAME, FILE_NAME).get()['Body'].read().decode("utf-8")
    assert body == '1,2,3,4'


@mock_s3
def test_download_all_files_as_zip():
    """Test download all files into zip. Faster than to folder!"""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    store = S3Storage(conn, BUCKET_NAME)
    store.upload_from_folder(FILE_PATH)
    downloader = S3Downloader(conn, BUCKET_NAME)
    downloader.download_all_files_as_zip(DOWNLOAD_PATH)
    for filename in os.listdir(DOWNLOAD_PATH):
        with ZipFile(Path(DOWNLOAD_PATH, filename)) as zf:
            assert zf.namelist() == ['file_name.csv', 'other_file.txt']
    shutil.rmtree(DOWNLOAD_PATH)
