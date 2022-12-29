import orc.settings
import boto3
import json

from orchestrator.automation.core import Delay


def get_client(service):
    client = boto3.client(service,
                          aws_access_key_id=orc.settings.AWS_KEY,
                          aws_secret_access_key=orc.settings.AWS_SECRET,
                          region_name=orc.settings.REGION
                          )
    return client


def send_request(msg, main_object, delay=Delay.NONE, parent_request_id=None):
    client = get_client('sqs')
    message_full_name = f'{msg.__class__.__module__}.{msg.__class__.__name__}'
    body = json.dumps(msg.__dict__)
    attributes = {
        'type': {
            'StringValue': main_object.__class__.__name__ ,
            'DataType': 'String'
        },
        'message': {
            'StringValue': message_full_name,
            'DataType': 'String'
        },
        'main_object': {
            'StringValue': str(main_object.id),
            'DataType': 'Number'
        },
    }
    if parent_request_id:
        attributes = { **attributes,
                       'parent_request_id': {
                            'StringValue': parent_request_id,
                            'DataType': 'String'
                            }
                    }
    client.send_message(QueueUrl=orc.settings.AWS_QUEUE_URL,
                        DelaySeconds=delay.value,
                        MessageBody=body,
                        MessageAttributes=attributes
                        )


def send_delay(main_object, request_id, delay=Delay.NONE):
    client = get_client('sqs')
    message_full_name = 'delay'
    body = str(delay.value)
    attributes = attributes = {
        'type': {
            'StringValue': main_object.__class__.__name__ ,
            'DataType': 'String'
        },
        'message': {
            'StringValue': message_full_name,
            'DataType': 'String'
        },
        'main_object': {
            'StringValue': str(main_object.id),
            'DataType': 'Number'
        },
        'request_id' : {
            'StringValue': str(request_id),
            'DataType': 'Number'
        }
    }

    client.send_message(QueueUrl=orc.settings.AWS_QUEUE_URL,
                        DelaySeconds=delay.value,
                        MessageBody=body,
                        MessageAttributes=attributes
                        )


class AmazonCloudService:

    def provision_instance(self, instance_type):
        client = get_client('ec2')

        return client.run_instances(
            ImageId="ami-075c1e3558b15afbb",
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName="shiggy"
        )

    def get_instance(self, instance):
        client = get_client('ec2')
        return client.describe_instances(InstanceIds=[instance])

    def get_instances(self, instances):
        client = get_client('ec2')
        return client.describe_instances(InstanceIds=instances)

    def terminate_instance(self, instance):
        client = get_client('ec2')
        return client.terminate_instances(
            InstanceIds=[instance]
        )

    def terminate_instances(self, instances):
        client = get_client('ec2')
        return client.terminate_instances(
            InstanceIds=instances
        )
