import os

import boto3

from dotenv import load_dotenv


load_dotenv()


AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


def upload_file_to_s3(
    file_bytes: bytes,
    s3_key: str,
    content_type: str | None,
):
    s3_client.put_object(
        Bucket=AWS_S3_BUCKET,
        Key=s3_key,
        Body=file_bytes,
        ContentType=content_type or "application/octet-stream",
    )

    return s3_key


def delete_file_from_s3(
    s3_key: str,
):
    if not s3_key:
        return

    s3_client.delete_object(
        Bucket=AWS_S3_BUCKET,
        Key=s3_key,
    )


def generate_resume_url(
    s3_key: str,
    expiration: int = 3600,
):
    if not s3_key:
        return None

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": AWS_S3_BUCKET,
            "Key": s3_key,
        },
        ExpiresIn=expiration,
    )