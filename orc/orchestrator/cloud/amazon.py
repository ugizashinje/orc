import orc.settings
import boto3

def get_ec2_client():
    client = boto3.client('ec2',
                              aws_access_key_id=orc.settings.AWS_KEY,
                              aws_secret_access_key=orc.settings.AWS_SECRET,
                              region_name=orc.settings.REGION
                              )
    return client


class AmazonCloudService:

    def _get_client(self, service):
        return boto3.client(service,
                             aws_access_key_id=orc.settings.AWS_KEY,
                             aws_secret_access_key=orc.settings.AWS_SECRET,
                             region_name=orc.settings.REGION
                             )

    def provision_instance(self, instance_type):

        client = self._get_client('ec2')

        return client.run_instances(
            ImageId="ami-075c1e3558b15afbb",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName="shiggy"
        )


    def get_instance(self, instance):
        client = self._get_client('ec2')
        return client.describe_instances(InstanceIds=[instance])

    def get_instances(self, instances):
        client = self._get_client('ec2')
        return client.describe_instances(InstanceIds=instances)

    def terminate_instance(self, instance):

        client = self._get_client('ec2')
        return client.terminate_instances(
            InstanceIds=[instance]
        )

    def terminate_instances(self, instances):

        client = self._get_client('ec2')
        return client.terminate_instances(
            InstanceIds=instances
        )