
from orchestrator.actors.server.amazon.terminate_server_message import TerminateServerMessage
from orchestrator.automation.core import Handle, Step, Actor


@Handle(TerminateServerMessage)
class TerminateServerActor(Actor):

    def first_step(self):
        return self.terminate

    @Step()
    def terminate(self):
        print('terminate')
