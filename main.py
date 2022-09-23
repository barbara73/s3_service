import time

from config import get_s3_resource
from src.s3interactions.s3_download import S3Downloader
from src.s3interactions.s3_interactions import list_buckets, create_bucket_name, create_new_bucket


def main():
    s3 = get_s3_resource()

    bucket_name = 'bkt-dfl-app-02-jesbaacc-tr_sds_deid_ct_images'
    # bucket_name = create_bucket_name(bucket_suffix='03-jesbaacc-a_test_source')
    # target_name = create_bucket_name(bucket_suffix='03-jesbaacc-a_test_target')
    # print(f'bucket_name: {bucket_name}')

    # my_bucket = create_new_bucket(s3, bucket_name)
    # print(f'bucket: {my_bucket}')

    # create_new_bucket(s3, target_name)

    list_buckets(s3)
    # list_bucket_objects(s3, target_name)

    path_to_files = 's3_downloads/'
    # my_csv_file = 'a_csv_file.csv'
    # my_text_file = 'a_text_file.txt'

    # upload files
    # start = time.time()
    # upload_files_from_folder(s3, bucket_name, path_to_files)
    # # upload_file(bucket_name, my_text_file, path_to_files)
    # end = time.time()
    # print(end - start)
    # download files
    # download_files_from_bucket(bucket_name, my_text_file)

    # copying between buckets
    # copying_between_buckets(source=bucket_name,
    #                         target=target_name)
    #
    # list_bucket_objects(s3, bucket_name)
    # list_bucket_objects(s3, target_name)

    # delete_all(s3, bucket_name)
    # delete_all(s3, target_name)
    # list_buckets(s3)


    # print(dcmread(download_in_memory(s3, bucket_name)))
    d = S3Downloader(s3, bucket_name)
    start = time.time()
    # d.download_all_files()
    # d.download_all_files_as_zip()
    print(d.get_file_in_memory('0a0a0beb-6e0e-44e2-89ac-c4a63b7faa39.dcm'))
    end = time.time()
    print(end - start)




if __name__ == '__main__':

    main()

    # ADVANCED OPERATIONS: see https://realpython.com/python-boto3-aws-s3/
