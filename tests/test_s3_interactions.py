import boto3
from moto import mock_s3

from src.s3interactions.s3_interactions import create_new_bucket, delete_all, list_buckets
from src.s3interactions.s3_interactions import list_bucket_objects, delete_bucket_objects
from src.s3interactions.s3_interactions import create_bucket_name, copying_between_buckets
from tests.conftest import BUCKET_NAME


def test_create_bucket_name():
    """Test the creation of bucket name."""
    assert create_bucket_name()[:12] == 'bkt-dfl-app-'
    assert create_bucket_name('abc')[:3] == 'abc'
    assert create_bucket_name(bucket_suffix='my_name') == 'bkt-dfl-app-my_name'


# @mock_s3
# def test_create_new_bucket():
#     """Test creation of bucket."""
#     conn = boto3.resource('s3', region_name='us-east-1')
#     assert create_new_bucket(conn, BUCKET_NAME) == conn.Bucket(name=BUCKET_NAME)


@mock_s3
def test_list_bucket_objects():
    """Test if objects of specific bucket are listed."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    obj = conn.Object(bucket_name=BUCKET_NAME, key='some_key')
    obj.put(Body='some_body')
    assert list_bucket_objects(conn, BUCKET_NAME) == ['some_key']


@mock_s3
def test_list_buckets():
    """Test if bucket names are listed."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    assert list_buckets(conn) == [BUCKET_NAME]


@mock_s3
def test_delete_bucket_objects():
    """Test if objects within buckets are deleted."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    obj = conn.Object(bucket_name=BUCKET_NAME, key='some_key')
    obj.put(Body='some_body')
    assert list_bucket_objects(conn, BUCKET_NAME) == ['some_key']
    delete_bucket_objects(conn, BUCKET_NAME)
    assert list_bucket_objects(conn, BUCKET_NAME) == []


@mock_s3
def test_delete_bucket():
    """Test if bucket with objects are deleted."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    assert delete_all(conn, BUCKET_NAME) is None


@mock_s3
def test_copying_between_buckets():
    """Test if copy between buckets works."""
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET_NAME)
    obj = conn.Object(bucket_name=BUCKET_NAME, key='some_key')
    obj.put(Body='some_body')
    conn.create_bucket(Bucket='target')
    copying_between_buckets(conn, BUCKET_NAME, 'target')
    assert list_bucket_objects(conn, BUCKET_NAME) == list_bucket_objects(conn, 'target')
