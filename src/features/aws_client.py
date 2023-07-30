from PIL import Image
import io
import boto3
import os
import json
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
from botocore.exceptions import ClientError
import logging


class AwsClient:
    """Sends and receives data to/from AWS S3 bucket"""
    def __init__(self, bucket: str) -> None:
        load_dotenv()
        self.aws_access_key_id = os.getenv('env_aws_access_key_id')
        self.aws_secret_access_key = os.getenv('env_aws_secret_access_key')
        self.bucket = bucket

        self.s3_client = boto3.resource(
            's3',
            region_name='us-east-1',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

        self.lambda_client = boto3.client(
            'lambda',
            region_name='us-east-1',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

    def send_image(self, file_dir: Path, image_name: str) -> None:
        """Sends image to S3 bucket from file_dir"""
        file_path = file_dir / image_name
        self.s3_client.Bucket(self.bucket).upload_file(file_path, Key=image_name)

    def get_files_list(self) -> list[str]:
        """Loads list of files from S3 bucket"""
        response = self.lambda_client.invoke(
            FunctionName='get_list_of_items',
            InvocationType='RequestResponse')

        json_string = response['Payload'].read().decode()
        files_list = json.loads(json_string)['body']
        return files_list

    def get_image_from_s3(self, filename: str) -> Image:
        """Loads image in PIL.Image format from S3 bucket"""
        try:
            image = self.s3_client.Bucket(self.bucket).Object(filename)
            img_data = image.get().get('Body').read()
            return Image.open(io.BytesIO(img_data))
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                logging.error('NoSuchKey error - no object found - returning None')
                st.markdown("Error, no object found!")
            else:
                raise

    def lambda_crop_image(self, filename: str, coords: list[int]) -> None:
        """Invokes lambda function to crop and save image in S3 bucket"""
        payload_dict = {'filename': filename, 'coordinates': coords}
        response = self.lambda_client.invoke(
            FunctionName='crop_images',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_dict))

        json_string = response['Payload'].read().decode()
        response = json.loads(json_string)['body']
        st.markdown(response)
        logging.info(response)
