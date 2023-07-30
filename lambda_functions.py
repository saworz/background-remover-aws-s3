# Get files list Lambda function:
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id='XXXXXXXXXXXXXX',
        aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXX'

    )

    my_bucket = s3.Bucket('backgr-remover-swz')
    files = []
    for my_bucket_object in my_bucket.objects.all():
        files.append(my_bucket_object.key)

    return {
        'statusCode': 200,
        'body': files
    }


# Load, crop and save image Lambda function:
import json
import boto3
import os.path
import io
from PIL import Image


def lambda_handler(event, context):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id='XXXXXXXXXXX',
        aws_secret_access_key='XXXXXXXXXXXXXXXXXXX'

    )

    client = boto3.client('s3')

    my_bucket = s3.Bucket('backgr-remover-swz')

    filename = event["filename"]
    splited_filename = filename.split(".")

    for file in my_bucket.objects.all():
        if filename in file.key:
            resp = "exists"
            break
        resp = "incorrect input"

    if resp == "exists":
        obj = my_bucket.Object(event["filename"])
        response = obj.get()
        file_stream = response['Body']
        im = Image.open(file_stream)
        x0, y0, x1, y1 = event["coordinates"]
        cropped_image = im.crop((x0, y0, x1, y1))
        new_filename = splited_filename[0] + "_cut." + splited_filename[1]

        img_byte_arr = io.BytesIO()
        cropped_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        client.put_object(Bucket="backgr-remover-swz", Key=new_filename, Body=img_byte_arr)
        resp = "Succesfully uploaded file to S3!"

    return {
        'statusCode': 200,
        'body': json.dumps(resp)
    }
