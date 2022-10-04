import json
import logging
import orc.settings
import orchestrator.constants
import orchestrator.cloud.amazon
from orchestrator.models import ServerRequest
from orchestrator.automation.core import mapping


class Processor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = orchestrator.cloud.amazon.get_client('sqs')
        self.message_queue_url = orc.settings.AWS_QUEUE_URL

    def digest(self, msg):
        attributes = msg.get('MessageAttributes',{})
        if not attributes:
            self.logger.error(f'no attributes in msg: {msg}')
        msg_body = json.loads(msg['Body'])
        actor = mapping[attributes['message']['StringValue']]()
        actor.input = msg_body
        actor.data = {}
        first_step = actor.first_step()
        actor.context = { 'current_step': first_step.func.__name__,
                          'main_object': attributes['main_object']["StringValue"] }
        actor.before_all()

        request = ServerRequest.objects.create(
            server_id = int(attributes["main_object"]["StringValue"]),
            message=attributes['message'],
            status=orchestrator.constants.SERVER_REQUEST.Status.PENDING,
            body={'input': msg_body, 'data': actor.data, 'context': actor.context}
        )

        try:
            next_step = first_step()
        except Exception as e:
            self.logger.error(f'Actor {actor.__class__} failed', exc_info=True)

        self.client.delete_message_batch(
            QueueUrl=self.message_queue_url,
            Entries=[{'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}]
        )

    def get_message(self):
        response = self.client.receive_message(QueueUrl=self.message_queue_url, WaitTimeSeconds=10, MaxNumberOfMessages=1, MessageAttributeNames=['All'])
        return response.get('Messages', [])