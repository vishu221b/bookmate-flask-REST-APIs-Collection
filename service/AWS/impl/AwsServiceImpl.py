from . import AwsServiceBase
import os
import boto3


class AwsServiceBaseImpl(AwsServiceBase):

    def get_session(self):
        return boto3.Session(
            aws_access_key_id=os.environ.get('AWS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_KEY_SECRET'),
        )

    def get_aws_resource(self, resource: str):
        return self.get_session().resource(resource)

    def upload_file_to_s3(self, **params):
        print(f"DEBUG: s3 POST Request params: {params}")
        s3 = self.get_aws_resource('s3')
        response = s3.Bucket(os.environ.get('AWS_BUCKET')).put_object(
            Key=f"{params.get('repoKey')}/{params.get('fileName')}",
            Body=params.get('fileContent'),
            ContentType=params.get('fileContentType'),
            ContentDisposition='inline',
            ACL=params.get('contentACL')
        )
        print(f"DEBUG: s3 POST Request Response received: {response.get()}")
        return response.get()

    def get_file_from_s3(self, **params):
        print(f"DEBUG: s3 GET Request params: {params}")
        s3 = self.get_aws_resource('s3')
        response = s3.Bucket(os.environ.get('AWS_BUCKET')).Object(
            f"{params.get('repoKey')}/{params.get('fileName')}"
        ).get(IfMatch=params.get('eTag'))
        print(f"DEBUG: s3 GET Request Response: {response}")
        return response

    def replace_file_in_s3(self, repo_key: str, old_file_key: str, new_file_key: str):
        print(f"DEBUG: s3 PUT Request params: {repo_key}, {old_file_key}, {new_file_key}")
        s3 = self.get_aws_resource('s3')
        _old_file = f"{repo_key}/{old_file_key}"
        _new_file = f"{repo_key}/{new_file_key}"
        response = s3.Object(
            os.environ.get('AWS_BUCKET'), _new_file).copy_from(
            CopySource="{}/{}".format(os.environ.get('AWS_BUCKET'), _old_file))
        print(f"DEBUG: s3 PUT Request Response: {response}")
        s3.Object(os.environ.get('AWS_BUCKET'), _old_file).delete()
