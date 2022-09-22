from orchestrator.automation.automation import RequestActor
from orchestrator.automation.automation import Step


class TerminateServerActor(RequestActor):

    def starts_with(self):
        return self.terminate

    @Step()
    def terminate(self):
        print('terminate')
