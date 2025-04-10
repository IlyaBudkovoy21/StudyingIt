import boto3
import logging

from StudyingIt import settings

log = logging.getLogger("coding.s3")


class ClientS3:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {'aws_access_key_id': access_key, 'aws_secret_access_key': secret_key,
                       'endpoint_url': endpoint_url}
        self.bucket_name = bucket_name
        self.session = boto3.session.Session()

    def get_client(self):
        return self.session.client('s3', **self.config, verify=False)

    def upload_file(
            self,
            file_name: str,
            username: str,
            text: str,
            task_name: str
    ):
        client = self.get_client()
        check = client.list_objects_v2(Bucket=self.bucket_name, Prefix=f'{task_name}-folder/')
        if 'Contents' not in check:
            client.put_object(Bucket=self.bucket_name, Key=f'{task_name}-folder/')
        check = client.list_objects_v2(Bucket=self.bucket_name, Prefix=f'{task_name}-folder/{username}-folder/')
        if 'Contents' not in check:
            client.put_object(Bucket=self.bucket_name, Key=f'{task_name}-folder/{username}-folder/')
        try:
            client.put_object(
                Bucket=self.bucket_name,
                Key=f'{task_name}-folder/{username}-folder/{file_name}',
                Body=text)
        except:
            log.error("Can't put object to the storage")


client = ClientS3(
    access_key=settings.AWS_ACCESS_KEY_ID,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url="https://s3.storage.selcloud.ru",
    bucket_name="container-studying-2"
)
