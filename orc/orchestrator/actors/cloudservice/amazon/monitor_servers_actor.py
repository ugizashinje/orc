from orchestrator.automation.automation import RequestActor
from orchestrator.automation.automation import Step

class MonitorServersActor(RequestActor):

    def starts_with(self):
        return self.validate

    @Step()
    def validate(self):
        print('validate')