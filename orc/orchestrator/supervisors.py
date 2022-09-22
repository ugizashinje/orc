from orchestrator.automation.automation import Supervisor


class AmazonMonitorTokenSupervisor(Supervisor):
    message_class = AmazonMonitorTokenMessage
    actor_class = AmazonMonitorTokenActor