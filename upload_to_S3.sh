#!/bin/bash



UPLOADS_DIR=("lespaul" "telecaster" "stratocaster") 


S3_CMD="s3cmd"
S3_BUCKET=s3://egil-ic/


# looks at the destination before copying files over 
# and only copies over files that are new and updated. 
for DIR in "${UPLOADS_DIR[@]}"
do
$S3_CMD sync --acl-public  "$DIR" "$S3_BUCKET"
done
