import threading
import time
import logging
from orchestrator.automation.core import mapping
import orchestrator.cloud.amazon
import orchestrator.automation.amazon

class RequestMessage:
    pass

class RequestActor:
    pass


class DaemonThread:

    def __init__(self, name="Deamon thread", message_queue_url=None):
        self.logger = logging.getLogger(__name__)
        self.thread = threading.Thread(name=name, target=self, daemon=True)
        self.message_queue_url = message_queue_url
        self.client = orchestrator.cloud.amazon.get_client('sqs')
        self.processor = orchestrator.automation.amazon.Processor()
        self.thread.start()

    def __call__(self, *args, **kwargs):
        self.logger.debug('started listening for messages')
        while (True):
            time.sleep(1)
            messages = self.processor.get_message()
            for msg in messages:
                self.processor.digest(msg)
            if messages:
                self.logger.debug(f'received no:{len(messages)} messages')
            else:
                self.logger.debug('pooling' if len(messages) else f'recieved {len(messages)}')
