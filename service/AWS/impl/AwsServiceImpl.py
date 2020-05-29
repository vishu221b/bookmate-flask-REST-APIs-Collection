from . import AwsServiceBase
from config import AWS_KEY_ID, AWS_KEY_SECRET, AWS_BUCKET
import boto3


class AwsServiceBaseImpl(AwsServiceBase):

    def get_session(self):
        return boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_KEY_SECRET,
        )

    def get_aws_resource(self, resource: str):
        return self.get_session().resource(resource)

    def upload_file_to_s3(self, **params):
        s3 = self.get_aws_resource('s3')
        response = s3.Bucket(AWS_BUCKET).put_object(
            Key=f"{params.get('repoKey')}/{params.get('fileName')}",
            Body=params.get('fileContent'),
            ContentType=params.get('fileContentType'),
            ContentDisposition='inline',
            ACL=params.get('contentACL')
        )
        return response

    def get_file_from_s3(self, **params):
        s3 = self.get_aws_resource('s3')
        response = s3.Object(
            bucket_name=AWS_BUCKET,
            key=f"{params.get('repoKey')}/{params.get('fileName')}"
        ).get()
        return response.get('Body')

    def replace_file_in_s3(self, repo_key: str, old_file_key: str, new_file_key: str):
        s3 = self.get_aws_resource('s3')
        _old_file = f"{repo_key}/{old_file_key}"
        _new_file = f"{repo_key}/{new_file_key}"
        response = s3.Object(AWS_BUCKET, _new_file).copy_from(CopySource="{}/{}".format(AWS_BUCKET, _old_file))
        print(f"DEBUG: Response for s3 replacement - {response}")
        s3.Object(AWS_BUCKET, _old_file).delete()
