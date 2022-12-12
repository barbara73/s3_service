"""
S3Downloader

- download all files
- download single file
- download all files to zip (more efficient (times 2), than to save into folder)
- get file into memory

"""
import sys
from dataclasses import dataclass, field
from io import BufferedReader, BytesIO
from os import mkdir, path
from pathlib import Path
from zipfile import ZipFile
from boto3 import resource
from botocore.exceptions import ClientError


# TODO add here the root and sys.path add root to conftest?
@dataclass
class S3Downloader:
    """
    For downloading files from bucket.
    """
    s3: resource
    bucket_name: str
    export_id: str = field(default=None)

    def download_all_files(self, f_path: str) -> None:
        """
        Download all files from bucket.
        """
        for obj in self.s3.Bucket(self.bucket_name).objects.all():
            self.download_single_file(obj.key, f_path)

    def download_single_file(self, f_name: str, f_path: str = '../files/s3_downloads') -> None:
        """
        Download single file.
        """
        if not path.isdir(f_path):
            mkdir(f_path)

        self.s3.Object(self.bucket_name,
                       f_name).download_file(str(Path(f_path, f_name)))

    def download_all_files_as_zip(self, f_path: str = 'files/s3_downloads') -> None:
        """
        Download files to zip. Is much faster than
        """
        if not path.isdir(Path(f_path)):
            mkdir(Path(f_path))

        try:
            with ZipFile(f'{f_path}/{self.bucket_name}_{self.export_id}.zip', 'w') as zf:
                for obj in self.s3.Bucket(self.bucket_name).objects.all():
                    response = obj.get()
                    zf.writestr(obj.key, response['Body'].read())
        except ClientError as ex:
            raise ClientError(f'Cannot download file {obj.key}!') from ex
        zf.close()

    def get_file_in_memory(self, f_name: str) -> BytesIO:
        """
        Download file in memory for manipulation before saving somewhere.
        """
        # for obj in self.s3.Bucket(self.bucket_name).objects.all():
        response = self.s3.Object(self.bucket_name, f_name).get()
        print(response)
        fid_ = BufferedReader(response['Body']._raw_stream)
        read_in_memory = fid_.read()
        return BytesIO(read_in_memory)


if __name__ == '__main__':
    print(sys.path)