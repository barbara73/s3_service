# S3 Plugin

This package is for interacting with AWS S3.

## Requirements
- path to certificate
- user
- host
- password (encrypted)

## Setup
Set up PyCharm (see https://wiki.usz.ch/display/MDM/Setup+PyCharm). 
Make sure that you are in a virtual environment (see https://wiki.usz.ch/display/MDM/Setup+New+Project) and then install the packages from the `requirements.txt`:
```shell
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --cert="C:\your_path_to_certificates\.certificates\USZRootCA2.cer" --proxy="http://proxy.usz.ch:8080"
```

## Connection
You will need a .env file with your login details saved in the root of this package.
```text
S3_USER=usz_user_name
S3_PWD=usz_encrypted_pwd
S3_HOST=usz_host
CERTIFICATE=/etc/pki/ca-trust/source/anchors/USZ-Root-CA-2.pem
...
```
## S3 Interactions
- Create bucket name
- Create bucket
- List buckets
- List bucket objects
- Copy objects into other bucket
- Delete bucket objects
- Delete bucket

## S3 Storage
- Upload a single file from folder 
- Upload object in memory
- Upload all files at one from folder or zip file.

The in_memory file needs to be saved as follows for e.g. dicom files:
```python
in_memory_file = BytesIO()
content.save_as(in_memory_file, write_like_original=False)
```

## S3 Download
- Download single files into folder or into a zip file.