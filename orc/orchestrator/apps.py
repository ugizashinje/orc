from django.apps import AppConfig


class OrchestratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orchestrator'

    def ready(self):
        import orchestrator.automation.daemon
        dt = orchestrator.automation.daemon.DaemonThread()
        print('Orc loaded')