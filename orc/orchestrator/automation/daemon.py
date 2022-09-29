import threading
import time
import boto3
import orc.settings
import logging
from orchestrator.models import CloudService, CloudServiceProperty


class RequestMessage:
    pass

class RequestActor:
    pass


class DaemonThread:

    def __init__(self, name="Deamon thread"):
        self.logger = logging.getLogger(__name__)
        self.thread = threading.Thread(name=name, target=self, daemon=True)
        self.sqs = boto3.resource('sqs',
                             aws_access_key_id=orc.settings.AWS_KEY,
                             aws_secret_access_key=orc.settings.AWS_SECRET,
                             region_name=orc.settings.REGION
                             )
        self.queue = self.sqs.create_queue(QueueName=orc.settings.AWS_MESSAGE_QUEUE_NAME, Attributes={})
        self.message_queue_url = self.queue.url
        self.thread.start()

    def __call__(self, *args, **kwargs):
        self.logger.debug('started listening for messages')
        while (True):
            msgs = self.queue.receive_messages(QueueUrl=self.message_queue_url, WaitTimeSeconds=10)
            time.sleep(1)

            for msg in msgs:
                self.logger.debug(f'received {str(msg.body)}')
            if not msgs:
                self.logger.debug('pooling' if len(msgs) else f'recieved {len(msgs)}')
            else:
                self.logger.debug(f'received no:{len(msgs)} messages')
                self.sqs.meta.client.delete_message_batch(
                    QueueUrl=self.queue.url,
                    Entries=[{'Id': msg.message_id, 'ReceiptHandle': msg.receipt_handle} for msg in msgs]
                )
