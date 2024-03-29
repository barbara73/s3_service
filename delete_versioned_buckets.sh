#!/bin/bash

bucket=$1

set -e

echo "Removing all versions from $bucket"

versions=`aws s3api --endpoint-url https://s3url.ch list-object-versions --bucket $bucket --ca-bundle CA.pem |jq '.Versions'`
markers=`aws s3api --endpoint-url https://s3url.ch list-object-versions --bucket $bucket --ca-bundle CA.pem |jq '.DeleteMarkers'` 

echo "removing files"
for version in $(echo "${versions}" | jq -r '.[] | @base64'); do 
    version=$(echo ${version} | base64 --decode)

    key=`echo $version | jq -r .Key`
    versionId=`echo $version | jq -r .VersionId `
    cmd="aws s3api --endpoint-url https://s3url.ch delete-object --bucket $bucket --key $key --version-id $versionId --ca-bundle CA-2.pem"
    echo $cmd
    $cmd
done

echo "removing delete markers"
for marker in $(echo "${markers}" | jq -r '.[] | @base64'); do 
    marker=$(echo ${marker} | base64 --decode)

    key=`echo $marker | jq -r .Key`
    versionId=`echo $marker | jq -r .VersionId `
    cmd="aws s3api --endpoint-url https://s3url.ch delete-object --bucket $bucket --key $key --version-id $versionId --ca-bundle CA-2.pem"
    echo $cmd
    $cmd
done
