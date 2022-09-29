import logging
from django.apps import AppConfig


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
        dt = orchestrator.automation.daemon.DaemonThread()
