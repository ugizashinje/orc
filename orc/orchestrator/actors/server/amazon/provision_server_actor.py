from orchestrator.automation.automation import RequestActor
from orchestrator.automation.automation import Step


class ProvisionServerActor(RequestActor):

    def starts_with(self):
        return self.check_tokens

    @Step()
    def check_tokens(self):
        print('aaaaaaa')