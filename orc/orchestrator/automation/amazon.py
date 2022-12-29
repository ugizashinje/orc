import json
import logging

from redis import Redis

import orc.settings
import orchestrator.constants
import orchestrator.cloud.amazon
from orchestrator.automation.core import mappingMessages, mappingRequests, Delay, Actor


class Processor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = orchestrator.cloud.amazon.get_client('sqs')
        self.message_queue_url = orc.settings.AWS_QUEUE_URL
        self.redis = Redis()
    def digest(self, msg):
        attributes = msg.get('MessageAttributes',{})
        if not attributes:
            self.logger.error(f'no attributes in msg: {msg}')
        msg_body = json.loads(msg['Body'])

        initial_context = { 'main_object': attributes['main_object']["StringValue"] }

        requestType = attributes['type'].get('StringValue') if attributes.get('type') else None
        messageType = attributes['message']['StringValue']
        request_id = None
        if messageType == 'delay':
            request_id = int(attributes['request_id']['StringValue'])
        model, requestClass = mappingRequests.get(requestType)
        main_object = model.objects.filter(id=int(attributes['main_object']['StringValue'])).first()
        if main_object is None:
            self.logger.error(f'Unknown object {attributes["main_object"]["StringValue"]} received')

        if requestClass is None:
            self.logger.error(f'Unknown message {msg} received')
        else:
            if messageType == 'delay':
                request = requestClass.objects.filter(id=request_id).first()
            else:
                request = requestClass.objects.create(
                    object_id = main_object.id,
                    message=messageType,
                    status=orchestrator.constants.SERVER_REQUEST.Status.PENDING,
                    body={'input': msg_body, 'data': dict(), 'context': initial_context}
                )

            try:
                self.process(main_object, request)
            except Exception as e:
                self.logger.error('failed processing message', exc_info=True)
                request.status = orchestrator.constants.SERVER_REQUEST.Status.FAILED
                request.save(update_fields=['status', 'body'])
        self.client.delete_message_batch(
            QueueUrl=self.message_queue_url,
            Entries=[{'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}]
        )

    def get_message(self):
        response = self.client.receive_message(QueueUrl=self.message_queue_url, WaitTimeSeconds=10, MaxNumberOfMessages=1, MessageAttributeNames=['All'])
        messages = response.get('Messages', [])
        if messages:
            processed = self.redis.set(messages[0]['MessageId'], 'True', get=True, ex=10)
            if not processed:
                return messages
        return [];
    def process(self, main_object, request):
        actor = mappingMessages[request.message]()
        actor.main_object = main_object
        actor.input = request.body['input']
        actor.data = request.body['data']
        actor.before_all()
        current_step_name = request.body['context'].get('current_step',actor.first_step().func.__name__)
        current_step = getattr(actor, current_step_name)

        while True:
            request.status = orchestrator.constants.SERVER_REQUEST.Status.PROCESSING
            request.save(update_fields=['status'])
            kwargs = { **actor.input, **actor.data}
            response = current_step(**kwargs)
            if type(response) == tuple:
                current_step, delay = response
                request.body['context']['current_step'] = current_step.func.__name__
                request.body['data'] = actor.data
                request.save(update_fields=['body'])
                if delay is not Delay.NONE:
                    orchestrator.cloud.amazon.send_delay(actor.main_object, request.id, delay)
                    break
            elif response is Actor.COMPLETED:
                request.body['data'] = actor.data
                request.status = orchestrator.constants.SERVER_REQUEST.Status.COMPLETED
                request.save(update_fields=['body', 'status'])
                break
        return request
