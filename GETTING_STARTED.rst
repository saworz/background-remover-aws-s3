1. Configurating AWS

	1.1. S3 Bucket
	   You need to create your own S3 bucket and change it's name in AWS_CLIENT class ("backgr-remover-swz" in my case)
	1.2. Lambda functions.
	   I have created two separated Lambda functions - one to read contents of S3 bucket and one to load, crop and save image 
	   from S3. 
	   ---Code for Lambda functions in lambda_functions.py file---
	1.3. Create permissions (IAM Roles) - go to IAM Roles -> Users -> Add users -> Attach policies directly -> AmazonS3FullAccess,
	   AmazonS3ObjectLambdaExecutionRolePolicy, AWSLambdaRole and use access and secret keys from that IAM Role to connect to AWS clients.


2. Downloading model weights

    2.1. Create dir
        Create Background_remove_AmazonS3/saved_models/u2net/ dir and paste inside
        u2net.pth downloaded from https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view?pli=1