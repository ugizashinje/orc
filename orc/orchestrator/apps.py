import logging
from django.apps import AppConfig
import boto3
import orc.settings

class OrchestratorConfig(AppConfig):

    def __init__(self, app_name, app_module):
        self.logger = logging.getLogger(__name__)
        super().__init__(app_name, app_module)

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orchestrator'

    def ready(self):
        pass
        import orchestrator.automation.daemon
        import orchestrator.automation.register
        self.sqs = boto3.resource('sqs',
                             aws_access_key_id=orc.settings.AWS_KEY,
                             aws_secret_access_key=orc.settings.AWS_SECRET,
                             region_name=orc.settings.REGION
                             )
        queue = self.sqs.create_queue(QueueName=orc.settings.AWS_MESSAGE_QUEUE_NAME, Attributes={})

        dt = orchestrator.automation.daemon.DaemonThread(message_queue_url=queue.url)
