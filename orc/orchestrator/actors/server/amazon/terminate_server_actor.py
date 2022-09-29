
from orchestrator.actors.server.amazon.terminate_server_message import TerminateServerMessage
from orchestrator.automation.core import Handle, Step


@Handle(TerminateServerMessage)
class TerminateServerActor:

    def starts_with(self):
        return self.terminate

    @Step()
    def terminate(self):
        print('terminate')
